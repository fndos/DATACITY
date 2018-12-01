from osgeo import ogr
from django.contrib.gis.geos.collections import MultiPolygon, MultiLineString
from django.contrib.gis.geos.geometry import GEOSGeometry
import datetime

"""
Dado una constante ogr  que define
un tipo de geometria, esta funcion
retorna el  nombre de esa  tipo de
geometria
"""
def ogr_type_to_geometry_name(ogr_type):
	typesMap = {ogr.wkbUnknown:'Unknown',
		ogr.wkbPoint:'Point',
		ogr.wkbLineString:'LineString',
		ogr.wkbPolygon:'Polygon',
		ogr.wkbMultiPoint:'MultiPoint',
		ogr.wkbMultiLineString:'MultiLineString',
		ogr.wkbMultiPolygon:'MultiPolygon',
		ogr.wkbGeometryCollection:'GeometryCollection',
		ogr.wkbNone:'None',
		ogr.wkbLinearRing:'LinearRing'}
	return typesMap.get(ogr_type)

"""
La funcion recibe una   geometria.
Si esa   geometria  es  Polygon, o 
LineString retorna un MultiPolygon
o MultiLineString
"""
def wrap_geos_geometry(geometry):
	if geometry.geom_type == "Polygon":
		return MultiPolygon(geometry)
	elif geometry.geom_type == "LineString":
		return MultiLineString(geometry)
	else:
		return geometry

"""
Dado el nombre de un  tipo de una   geometria,
retorna el nombre equivalente de esa geometria 
en PostGIS
"""
def calc_geometry_field(geometry_type):
	if geometry_type == "Polygon":
		return "geom_multipolygon"
	elif geometry_type == "LineString":
		return "geom_multilinestring"
	else:
		return "geom_" + geometry_type.lower()

"""
Dado  un vectorlayer.models.Attribute, un
vectorLayer.models.Feature  y el encoding
de  una  capa,  retorna el  valor  de ese 
atributo como string
"""
def getOGRFeatureAttribute(attr, feature, encoding):
	# se obtiene el nombre del atributo
	attr_name = str(attr.name)
	# si ese atributo no pertenece al feature
	# retorna un error
	if not feature.IsFieldSet(attr_name):
		return (True, None)

	# si el tipo de dato del attribute 
	# es string, este flag es verdadero
	needs_encoding = False

	# Dependiendo del tipo de dato del attr
	# se obtiene el value, y se transforma 
	if attr.type == ogr.OFTInteger:
		value = str(feature.GetFieldAsInteger(attr_name))
	elif attr.type == ogr.OFTIntegerList:
		value = repr(feature.GetFieldAsIntegerList(attr_name))
	elif attr.type == ogr.OFTReal:
		value = feature.GetFieldAsDouble(attr_name)
		value = "%*.*f" % (attr.width, attr.precision, value)
	elif attr.type == ogr.OFTRealList:
		values = feature.GetFieldAsDoubleList(attr_name)
		str_values = []
		for value in values:
			str_values.append("%*.*f" % (attr.width,attr.precision,value))
		value = repr(str_Values)
	elif attr.type == ogr.OFTString:
		value = feature.GetFieldAsString(attr_name)
		needs_encoding = True
	elif attr.type == ogr.OFTStringList:
		value = repr(feature.GetFieldAsStringList(attr_name))
		needs_encoding = True
	elif attr.type == ogr.OFTWideString:
		value = feature.GetFieldAsString(attr_name)
		needs_encoding = True
	elif attr.type == ogr.OFTDate:
		parts = feature.GetFieldAsDateTime(attr_name)
		year,month,day,hour,minute,second,tzone = parts
		value = "%d,%d,%d,%d" % (year,month,day,tzone)
	elif attr.type == ogr.OFTTime:
		parts = feature.GetFieldAsDateTime(attr_name)
		year,month,day,hour,minute,second,tzone = parts
		value = "%d,%d,%d,%d" % (hour,minute,second,tzone)
	elif attr.type == ogr.OFTDateTime:
		parts = feature.GetFieldAsDateTime(attr_name)
		year,month,day,hour,minute,second,tzone = parts
		value = "%d,%d,%d,%d,%d,%d,%d,%d" % (year,month,day,
		                                     hour,minute,
		                                     second,tzone)
	elif attr.type== ogr.OFTInteger64:
		value = str(feature.GetFieldAsInteger64(attr_name))
	elif attr.type== ogr.OFTInteger64List:
		value = repr(feature.GetFieldAsInteger64List(attr_name))
	else:
		return (False, "Unsupported attribute type: " +
                       str(attr.type))
    
    # si se requiere encoding
	if needs_encoding:
		try:
			value = value.decode(encoding)
		except UnicodeDecodeError:
			return (False, "Unable to decode value in " +
						repr(attr_name) + " attribute.&nbsp; " +
						"Are you sure you're using the right " +
						"character encoding?")
	return (True, value)

"""
Realiza lo contrario que wrap_geos_geometry
"""
def unwrap_geos_geometry(geometry):
	if geometry.geom_type in ["MultiPolygon","MultiLineString"]:
		if len(geometry) == 1:
			geometry = geometry[0]
	return geometry

"""
Dado un vectorlayer.models.Attribute, 
un el valor  del attr, un ogr.Feature 
y el encoding  de  una capa, setea el 
value al feature
"""
def set_ogr_feature_attribute(attr, value, feature, encoding):
	attr_name = str(attr.name)
	if value == None:
		feature.UnsetField(attr_name)
		return
	if attr.type == ogr.OFTInteger:
		feature.SetField(attr_name, int(value))
	elif attr.type == ogr.OFTIntegerList:
		integers = eval(value)
		feature.SetFieldIntegerList(attr_name, integers)
	elif attr.type == ogr.OFTReal:
		feature.SetField(attr_name, float(value))
	elif attr.type == ogr.OFTRealList:
		floats = []
		for s in eval(value):
			floats.append(eval(s))
		feature.SetFieldDoubleList(attr_name, floats)
	elif attr.type == ogr.OFTString:
		feature.SetField(attr_name, value.encode(encoding))
	elif attr.type == ogr.OFTStringList:
		strings = []
		for s in eval(value):
			strings.append(s.encode(encoding))
		feature.SetFieldStringList(attr_name, strings)
	elif attr.type == ogr.OFTWideString:
		feature.SetField(attr_name,value.encode(encoding))
	elif attr.type == ogr.OFTDate:
		parts = value.split(",")
		year = int(parts[0])
		month = int(parts[1])
		day = int(parts[2])
		tzone = int(parts[3])
		feature.SetField(attr_name, year, month, day, 0, 0, 0, tzone)
	elif attr.type == ogr.OFTTime:
		parts = value.split(",")
		hour = int(parts[0])
		minute = int(parts[1])
		second = int(parts[2])
		tzone = int(parts[3])
		feature.SetField(attr_name, 0, 0, 0, hour, minute, second, tzone)
	elif attr.type == ogr.OFTDateTime:
		parts = value.split(",")
		year  = int(parts[0])
		month = int(parts[1])
		day = int(parts[2])
		hour = int(parts[3])
		minute = int(parts[4])
		second = int(parts[5])
		tzone = int(parts[6])
		feature.SetField(attr_name, year, month, day, hour, minute, second, tzone)
	elif attr.type == ogr.OFTInteger64:
		feature.SetField(attr_name, int(value))
	elif attr.type == ogr.OFTInteger64List:
		integers = eval(value)
		feature.SetFieldIntegerList(attr_name, integers)

"""
Dado  un vectorlayer.models.Attribute, un
vectorLayer.models.Feature  y el encoding
de  una  capa,  retorna el  valor  de ese 
atributo como su tipo de dato real
"""     
def getAttrValue(attr, value, encoding):
	attr_name = str(attr.name)
	if value == None:
		return value

	if attr.type == ogr.OFTInteger:
		return int(value);
	elif attr.type == ogr.OFTIntegerList:
		integers = eval(value)
		return integers
	elif attr.type == ogr.OFTReal:
		return float(value)
	elif attr.type == ogr.OFTRealList:
		floats = []
		for s in eval(value):
			floats.append(eval(s))
		return floats
	elif attr.type == ogr.OFTString:
		return value.encode(encoding)
	elif attr.type == ogr.OFTStringList:
		strings = []
		for s in eval(value):
			strings.append(s.encode(encoding))
		return strings
	elif attr.type == ogr.OFTWideString:
		return value.encode(encoding)
	elif attr.type == ogr.OFTDate:
		parts = value.split(",")
		year = int(parts[0])
		month = int(parts[1])
		day = int(parts[2])
		tzone = int(parts[3])
		result = datetime.datetime(year=year,month=month,day=day,tzinfo=tzone);
		return result
	elif attr.type == ogr.OFTTime:
		parts = value.split(",")
		hour = int(parts[0])
		minute = int(parts[1])
		second = int(parts[2])
		tzone = int(parts[3])
		result = datetime.datetime(hour=hour,minute=minute,second=second,tzinfo=tzone);
		return result
	elif attr.type == ogr.OFTDateTime:
		parts = value.split(",")
		year  = int(parts[0])
		month = int(parts[1])
		day = int(parts[2])
		hour = int(parts[3])
		minute = int(parts[4])
		second = int(parts[5])
		tzone = int(parts[6])
		result = datetime.datetime(year=year,month=month,day=day,hour=hour,minute=minute,second=second,tzinfo=tzone)
		return result;
	elif attr.type==ogr.OFTInteger64:
		return int(value);
	elif attr.type == ogr.OFTInteger64List:
		integers = eval(value)
		return integers

	return None;

