# -*- encoding: utf-8 -*-
import json
import psycopg2
import random
from datetime import datetime
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# ejecuta los querys insert
def executeInsert(dbParams,query,queryParams):
	conn = None
	try:
		conn = psycopg2.connect(host=dbParams["host"],
								port=dbParams["port"],
								user=dbParams["user"],
								password=dbParams["password"],
								dbname=dbParams["dbname"])
		cursor = conn.cursor()

		cursor.execute(query,queryParams)
		conn.commit()
	except Exception as e:
		error_str = "Fallo la base de datos" + str(e);
		return error_str;
	finally:
		if conn:
			conn.close()

	return None 

# ejecuta los querys select
def executeSelect(dbParams,query,queryParams):
	conn = None
	try:
		conn = psycopg2.connect(host=dbParams["host"],
								port=dbParams["port"],
								user=dbParams["user"],
								password=dbParams["password"],
								dbname=dbParams["dbname"])
		cursor = conn.cursor()

		cursor.execute(query,queryParams)
		result = cursor.fetchall();
		return result,None
	except Exception as e:
		error_str = "Fallo la base de datos" + str(e);
		return None,error_str;
	finally:
		if conn:
			conn.close() 

# obtiene los datos de la base
def getData(dbParams):
	# se recuperan las estaciones
	query = 'SELECT s.id,st.id,st.brand FROM "timeSeries_station" as s, "timeSeries_stationtype" as st '
	query = query + 'WHERE s."stationType_id" = st.id'
	stations_db,error = executeSelect(dbParams,query,[])

	stations = []
	for station_db in stations_db:
		station = {}
		station["id"] = station_db[0]
		station["stationType_id"] = station_db[1]
		station["brand"] = station_db[2]
		stations.append(station)


	# se recuperan los tipos de estaciones
	query = 'SELECT id,brand FROM "timeSeries_stationtype"';
	stationTypes_db,error = executeSelect(dbParams,query,[])
	stationTypes = []
	for stationType_db in stationTypes_db:
		stationType = {}
		stationType["id"] = stationType_db[0]
		stationType["brand"] = stationType_db[1]
		stationType["variables"] = []
		stationTypes.append(stationType)

	# se recuperan las variables de los tipos de estaciones
	for stationType in stationTypes:
		query = 'SELECT v.id,v.name,v.datatype FROM "timeSeries_stationtype" as s,"timeSeries_variable" as v,'
		query = query + '"timeSeries_stationtype_variables" as sv WHERE sv.stationtype_id=s.id '
		query = query + 'and sv.variable_id = v.id'
		variables_db,error = executeSelect(dbParams,query,[])
		for variable_db in variables_db:
			variable = {}
			variable["id"]=variable_db[0]
			variable["name"]=variable_db[1]
			variable["datatype"]=variable_db[2]
			stationType["variables"].append(variable)

	return stations,stationTypes

# crea una lista de fechas desde ini_year hasta end_year
def createTimes(ini_year,end_year):
	years = range(ini_year,end_year+1)
	months = range(1,13)
	days = range(1,28)
	times = []
	for year in years:
		for month in months:
			for day in days:
				t = datetime(year, month, day)
				times.append(t)

	return times

# crea un diccionario con valores (readings)
def createValues(variables):
	values = {}
	for variable in variables:
		id_variable = variable["id"]
		value = None
		if (variable["datatype"]=="float"):
			value = random.uniform(0, 60)
		if (variable["datatype"]=="boolean"):
			value = bool(random.getrandbits(1))
		if (variable["datatype"]=="string"):
			value = "string"
		values[id_variable]=value
	return json.dumps(values)

# genera y guarda series de tiempo
def saveTimeSeries(stations,stationTypes):
	
	for station in stations:
		stationtype_id = station["stationType_id"]
		station_id = station["id"]
		variables= None
		for stationType in stationTypes:
			if(stationType["id"]==stationtype_id):
				variables = stationType["variables"]

		print "Estacion ",station_id
		# genera fechas desde el 2015 al 2018
		times = createTimes(2015,2018)
		query = 'INSERT INTO "timeSeries_measurement"("idStation_id","ts","readings") VALUES'
		params = []
		for t in times:
			values = createValues(variables);
			query = query + '(%s::integer,%s::timestamp,%s::json),'
			params.append(station_id)
			params.append(t)
			params.append(values)

		query = query[:-1]
		result = executeInsert(dbParams,query,params)
		if result==None:
			print "Serie guardada"
		else:
			print result

# genera y guarda series de tiempo
def saveTimeSeriesDynamic(stations,stationTypes, dbParams):
	
	for station in stations:
		#ask to user if they want to continue
		answer = input("Ingrese 0 si desea terminar, 1 si desea continuar\n")
		if(int(answer)==0):
			return
		#else
		stationtype_id = station["stationType_id"]
		stationType_brand = None
		station_id = station["id"]
		variables= None
		for stationType in stationTypes:
			if(stationType["id"]==stationtype_id):
				variables = stationType["variables"]
				stationType_brand = stationType["brand"]

		print "Estacion ",station_id
		# genera fechas dinamicamente
		print("Generando datos para la estacion marca "+ stationType_brand + "y id "+ str(station_id) )
		start_year = input("Ingrese año de inicio\n")
		end_year = input ("Ingrese año final\n")
		times = createTimes(int(start_year),int(end_year))
		query = 'INSERT INTO "timeSeries_measurement"("idStation_id","ts","readings") VALUES'
		params = []
		for t in times:
			values = createValues(variables);
			query = query + '(%s::integer,%s::timestamp,%s::json),'
			params.append(station_id)
			params.append(t)
			params.append(values)

		query = query[:-1]
		result = executeInsert(dbParams,query,params)
		if result==None:
			print "Serie guardada"
		else:
			print result


if __name__ == "__main__":
	file_name = "/home/manager/RESCLIMA/dbparams.json"
	dbParams = None
	with open(file_name) as data_file:
		dbParams = json.load(data_file)

	print "Los parametros de la base de datos: ",dbParams
	
	stations, stationTypes = getData(dbParams)
	print "Las estaciones obtenidas", stations
	print "Los tipos de estaciones con sus variables: ", stationTypes
	print "Creando series de tiempo..."
	saveTimeSeries(stations,stationTypes)

