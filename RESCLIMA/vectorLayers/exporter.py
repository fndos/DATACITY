# -*- encoding: utf-8 -*-
import os, os.path, tempfile, zipfile
import shutil, traceback
from osgeo import ogr
from models import VectorLayer, Attribute, Feature, AttributeValue
import utils
from django.contrib.gis.geos.geometry import GEOSGeometry
from osgeo import osr
from django.http import HttpResponse
from wsgiref.util import FileWrapper
import json

"""
Obtiene los  datos de una capa 
vectorial, crea un shapefile y 
retorna un HttpResponse con el 
archivo
"""
def export_shapefile(vectorlayer):
	# crea un directorio temporal
	dst_dir = tempfile.mkdtemp()
	# ruta del shapefile
	dst_file = os.path.join(dst_dir, vectorlayer.filename)
	dst_file = dst_file.encode('utf-8')
	# obtiene el sistema de coordenadas
	# original de la capa
	dst_spatial_ref = osr.SpatialReference()
	dst_spatial_ref.ImportFromWkt(vectorlayer.srs_wkt)
	
	# con la libreria osr se crea el shapefile
	driver = ogr.GetDriverByName("ESRI shapefile")
	datasource = driver.CreateDataSource(dst_file)	
	layer = datasource.CreateLayer(vectorlayer.filename.encode('utf-8'),dst_spatial_ref)

	# se guardan los atributos de la capa en 
	# el archivo
	for attr in vectorlayer.attribute_set.all():
		field = ogr.FieldDefn(str(attr.name), attr.type)
		field.SetWidth(attr.width)
		field.SetPrecision(attr.precision)
		layer.CreateField(field)

	# En la base de datos, los features de la capa
	# se guardan con un sistema de coordenadas
	# con srid = 4326. Los features seran transformados
	# a su sistema de coordenadas original
	src_spatial_ref = osr.SpatialReference()
	src_spatial_ref.ImportFromEPSG(4326)
	coord_transform = osr.CoordinateTransformation(src_spatial_ref, dst_spatial_ref)
	# se obtiene el tipo de geometria (punto, linea, poligono, etc)
	geom_field = utils.calc_geometry_field(vectorlayer.geom_type)

	# se recorren los features de la capa vectorial
	# se tranforman al sistema de referencia original
	# y se guardan en el archivo
	for feature in vectorlayer.feature_set.all():
		geometry = getattr(feature, geom_field)
		geometry = utils.unwrap_geos_geometry(geometry)
		dst_geometry = ogr.CreateGeometryFromWkt(geometry.wkt)
		dst_geometry.Transform(coord_transform)
		dst_feature = ogr.Feature(layer.GetLayerDefn())
		dst_feature.SetGeometry(dst_geometry)
		# se le agregan los valores no geometricos
		# al feature
		for attr_value in feature.attributevalue_set.all():
			utils.set_ogr_feature_attribute(
				attr_value.attribute,
				attr_value.value,
				dst_feature,
				vectorlayer.encoding)

		# se agrega el feature al archivo
		layer.CreateFeature(dst_feature)
		dst_feature.Destroy()

	datasource.Destroy()

	# se crea un zip y se envia el archivo

	vectorlayer_name = os.path.splitext(vectorlayer.filename)[0]
	zip_dst = dst_dir + "_zip";
	# se crea un zip con los archivos del shapefile
	zip_dst = shutil.make_archive(zip_dst, 'zip', dst_dir)
	# se elimina la carpeta temporal
	shutil.rmtree(dst_dir)
	# se lee el zip y se lo envia al usuario
	zip_file = open(zip_dst,"r")

	f = FileWrapper(zip_file)
	response = HttpResponse(f, content_type="application/zip")
	response['Content-Disposition'] = "attachment; filename=" + vectorlayer_name + ".zip"
	
	return response


"""
Obtiene los  datos d e una capa 
vectorial,  crea un diccionario
que   contiene un  geojson y lo
retorna 
"""
def export_geojson(vectorlayer):
	geojson = {}
	geojson["type"] = "FeatureCollection";
	bbox = vectorlayer.bbox;
	geojson["bbox"] = bbox.geojson;
	geojson["crs"] = {"type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" }}
	geojson["features"] = []
		
	geom_field = utils.calc_geometry_field(vectorlayer.geom_type)
	for feature in vectorlayer.feature_set.all():
		geometry = getattr(feature, geom_field)
		geometry = utils.unwrap_geos_geometry(geometry)
		dst_geometry = ogr.CreateGeometryFromWkt(geometry.wkt)
		feature_json = {}
		feature_json["type"]="Feature";
		geometry_json = dst_geometry.ExportToJson();
		feature_json["geometry"] = json.loads(geometry_json);
		feature_json["properties"] = {};
		geojson["features"].append(feature_json);
		for attr_value in feature.attributevalue_set.all():
			attr = attr_value.attribute;
			attr_name = attr_value.attribute.name;
			value = attr_value.value;
			value = utils.getAttrValue(attr,value,vectorlayer.encoding)
			feature_json["properties"][attr_name] = value;
			
	return geojson

