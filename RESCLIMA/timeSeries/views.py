from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from wsgiref.util import FileWrapper
from models import StationType, Station, Variable
from django.contrib.gis.geos import Point
from django.contrib.auth.decorators import login_required
from tasks import parseHOBOFile
from RESCLIMA import settings
from django.db import connection
import os
import time
import datetime
import json
import shutil
import tempfile

'''
Vista  que  retorna una  Pagina home 
de las series de tiempo, se muestran 
las opciones disponibles
'''
@login_required(login_url='noAccess')
def home(request):
	return render(request,"home_series.html")

'''
Funcion usada para ingresar una estacion.
Recibe un  diccionario con  los atributos
de  la  estacion.  Retorna None si no hay
errores,   caso   contrario   retorna  un
mensaje de error.
'''
def addStation(data):
	try:
		stationType_id = int(data["stationType"]);
		serialNum = data["serialNum"];
		latitude = float(data["latitude"]);
		longitude = float(data["longitude"]);
		frequency = data["frequency"];
		token = data["token"];

		# se recupera el tipo de estacion
		stationType = StationType.objects.get(id=stationType_id);
		automatic = stationType.automatic;
		# se crea una estacion
		station = Station();
		station.serialNum = serialNum;
		station.location = Point(longitude,latitude);
		station.active = True;
		station.stationType = stationType;

		# si la estacion es automatica
		# se agregan la frecuencia
		# y el token
		if(automatic==True):
			if(frequency == "" or token == ""):
				return "Error: faltan argumentos";
			frequency = float(frequency);
			if(frequency<=0):
				return "Error: frecuencia debe ser mayor que cero"
			station.frequency = frequency;
			station.token = token;

		station.save();
	except Exception as e:
		return "Error " + str(e)
	return None

'''
Vista que retorna una  Pagina que  permite
ingresar una nueva estacion. Se implementa
el metodo GET y POST.  Con GET  se retorna
la pagina y con POST se guarda la estacion
ingresada.
'''
@login_required(login_url='noAccess')
def import_station(request):
	if request.method == "GET":
		station_types = StationType.objects.all()
		options = {'stationTypes':station_types}
		return render(request, 'import_station.html',options)
	elif request.method == "POST":
		err_msg = addStation(request.POST);
		return HttpResponse(err_msg);


"""
Funcion auxiliar, crea un nombre de
archivo, usando  la hora actual del
sistema, un prefijo y la extension
"""
def createFileName(prefix,extension):
	t = time.time()
	ts = datetime.datetime.fromtimestamp(t)
	timestamp_str = ts.strftime('%Y-%m-%d-%H-%M-%S')
	fileName = prefix + timestamp_str + extension
	return fileName


'''
Funcion auxiliar para guardar un archivo
Recibe un objeto UploadedFile de  django
y  guarda  el  archivo  en un directorio 
temporal. Retorna la ruta del archivo.
'''
def saveFile(ftemp):
	# directorio temporal del sistema
	temp_dir = settings.TEMPORARY_FILES_PATH
	fileName = createFileName("timeseries-",".csv")
	fullName = os.path.join(temp_dir,fileName)
	# si el objeto ftemp tiene el atributo 
	# temporary_file_path ya esta en el disco duro
	if (hasattr(ftemp,'temporary_file_path')):
		print "en el disco duro, serie de tiempo",fullName
		ftemp_path = ftemp.temporary_file_path()
		# mueve el archivo
		shutil.move(ftemp_path,fullName)
	else:
		print "en la memoria, serie de tiempo",fullName
		# el archivo esta en memoria y se debe 
		# escribir en el disco
		f = open(fullName,'w')
		for chunk in ftemp.chunks():
			f.write(chunk)
		f.close()

	return fullName

'''
Vista que permite subir un archivo csv con
las  series de  tiempo de una  estacion no
automatica. Se implementa  el metodo GET y
POST. Con GET se  retorna la pagina, y con
POST se guardan los datos del archivo.
'''
@login_required(login_url='noAccess')
def import_file(request):
	if request.method == "GET":
		station_types = StationType.objects.filter(automatic=False)
		params = {"stationTypes":station_types}
		return render(request, 'import_file.html', params)
	elif request.method == "POST":
		stationType_id = request.POST['stationType']
		stationType = StationType.objects.get(id=stationType_id)
		stationType_str = str(stationType)
		file_ptr = request.FILES['file']
		result = {}
		# dependiendo  del  tipo  de estacion  se 
		# procede con el adptador correspondiente
		if stationType_str == "HOBO-MX2300":
			# guarda el archivo
			fileName = saveFile(file_ptr)
			params = {}
			params["fileName"]=fileName
			print "se ejecuta la tarea en celery timeserie"
			task = parseHOBOFile.delay(params)
			result["task_id"] = task.id
			print "el id del task ", task.id
			result["err_msg"] = None
		else:
			result["task_id"] = None
			result["err_msg"] = "No se reconoce este tipo de estacion"
		return HttpResponse(json.dumps(result),content_type='application/json')

'''
Vista que retorna  una pagina
para visualizar las series de
tiempo
'''
def visualize(request):
	if request.method == 'GET':
		return render(request,"view_series.html");


"""
Vista que recupera informacion de una
variable, la retorna como json
"""
def get_variable_info(request,variable_id):
	try:
		variable = Variable.objects.get(id=variable_id)
		variable_json = {}
		variable_json["name"] = variable.name
		variable_json["unit"]=variable.unit
		variable_json["symbol"]=variable.symbol
		variable_json["datatype"]=variable.datatype
		return HttpResponse(json.dumps(variable_json),content_type='application/json')
	except Exception as e:
		return HttpResponse(status=404)

"""
Crea un query para recuperar de la
base de datos, las mediciones de 
una estacion de una variable, en 
un rango de fechas. Retorna el 
resultado del query
"""
def query_measurements(variable_id,station_id,
					ini_date,end_date,
					limit,offset):

	# se validan los parametros
	if(not(variable_id)):
		return None,"Falta argumento variable_id"
	if(not(station_id)):
		return None,"Falta argumento station_id"


	# del json se obtiene la variable_id (readings[variable_id])
	select_stm = 'SELECT readings::json->%s as measurements, ts, count(*) OVER() AS full_count '
	from_stm = 'FROM "timeSeries_measurement" as m '
	# se recuperan los measurements de la estacion 
	# cuyo readings contenga el id de la variable (variable_id)
	# readings={"variable_id":valor_variable}
	where_stm = 'WHERE "idStation_id"=%s and readings like \'%%"'+variable_id+'":%%\''
	# parametros de los placeholders query
	params = [variable_id,station_id]

	#si hay rango de fechas se agrega al where_stm
	if(ini_date):
		where_stm = where_stm + ' and ts>=%s'
		params.append(ini_date)
	
	if(end_date):
		where_stm = where_stm + ' and ts<=%s'
		params.append(end_date)

	qs = select_stm + from_stm + where_stm
	# se agrea order by
	qs = qs + ' ORDER BY ts'
	# si hay limit y offset
	# se agrega al query
	if(limit and offset):
		qs = qs + ' LIMIT %s OFFSET %s'
		params.append(limit)
		params.append(offset)

	with connection.cursor() as cursor:
		cursor.execute(qs, params)
		rows = cursor.fetchall()
		return rows,None


'''
Funcion que recupera las mediciones
de una estacion de una variable, en
un rango de fechas, retorna un dict
con los resultados
'''
def get_measurements_dict(variable_id,station_id,
					ini_date,end_date,
					limit,offset):

	# recupera los datos de la base de datos
	rows,error = query_measurements(variable_id,station_id,
					   ini_date,end_date,
					   limit,offset)

	if error:
		return None,error


	measurements = []
	full_count = 0

	for row in rows:
		m = {}
		m["value"] = row[0]
		m["ts"] = row[1]
		measurements.append(m)
		full_count = row[2]

	return {"measurements":measurements,"full_count":full_count},None


'''
Funcion que recupera las mediciones
de una estacion de una variable, en
un rango de fechas
'''
def get_measurements_csv(variable,station,
					ini_date,end_date,fileName):

	variable_id = str(variable.id)
	station_id = str(station.id)

	# recupera los datos de la base de datos
	rows,error = query_measurements(variable_id,station_id,
					   ini_date,end_date,
					   None,None)
	if error:
		return None,error

	f = open(fileName,'w')
	header_variable = "Variable:%s,Unit:%s\n"%(variable.name,variable.unit)
	header_variable=header_variable.encode("utf-8")
	f.write(header_variable)
	
	station_attr = (station.serialNum,station.location.x,station.location.y)
	header_station = "Station:%s,lon:%s,lat%s\n"%station_attr
	header_station = header_station.encode("utf-8")
	f.write(header_station)
	
	columns = "timestamp UTC-0\tvalue\n"
	f.write(columns)

	for row in rows:
		line = "%s\t%s\n"%(row[1],row[0])
		f.write(line)


"""
Vista que retorna las mediciones
de una estacion de una variable, 
en un rango de fechas
"""
def get_measurements(request):
	responseData = {'measurements': [], 'dates': [], 'variable_id': '', 'station_id': ''}
	if request.method != 'GET':
		return HttpResponse(status=500)

	# recupera variables del query string
	variable_id = request.GET.get('variable_id',None)
	station_id = request.GET.get('station_id',None)
	ini_date = request.GET.get('ini_date',None)
	end_date = request.GET.get('end_date',None)
	limit = request.GET.get('limit',None)
	offset = request.GET.get('offset',None)

	if(not(variable_id)):
		return HttpResponse(status=500)
	if(not(station_id)):
		return HttpResponse(status=500)

	# se recuperan los datos de la base de datos
	data,error = get_measurements_dict(variable_id,station_id,
								 ini_date,end_date,
								 limit,offset)

	if error:
		return HttpResponse(status=500)

	return JsonResponse(data)

"""
Vista que recupera las mediciones de 
una variable de todas las estaciones
que  se  envien en  el  request. Las 
mediciones se  guardan  en  archivos
csv y se crea un zip con todo
"""
def download_measurements(request):
	ini_date = request.GET.get('ini_date',None)
	end_date = request.GET.get('end_date',None)
	variable_str = request.GET.get('variable',None)

	i = variable_str.find("[")
	j = variable_str.find("]")

	if(i==-1 or j==-1):
		return HttpResponse(status=500)

	variable_id = variable_str[:i]
	stations_str = variable_str[i+1:j]
	stations_id = stations_str.split(",")

	# recupera la variable
	variable = Variable.objects.get(pk=variable_id);


	# se crea una carpeta temporal
	dst_dir = tempfile.mkdtemp()
	# por cada estacion se crea un archivo
	for station_id in stations_id:
		# se recupera la estacion
		station = Station.objects.get(pk=station_id)
		fileName = os.path.join(dst_dir,"variable_"+station_id+".csv")
		get_measurements_csv(variable,station,ini_date,end_date,fileName)

	# se comprime la carpeta
	zip_dst = dst_dir + "_zip";
	# se crea un zip con los archivos del shapefile
	zip_dst = shutil.make_archive(zip_dst, 'zip', dst_dir)
	# se elimina la carpeta temporal
	shutil.rmtree(dst_dir)
	# se lee el zip y se lo envia al usuario
	zip_file = open(zip_dst,"r")

	f = FileWrapper(zip_file)
	response = HttpResponse(f, content_type="application/zip")
	prefix = "variable_"+variable_id+"_"
	fileName = createFileName(prefix,".zip")
	response['Content-Disposition'] = "attachment; filename=" + fileName
	
	return response

