# -*- encoding: utf-8 -*-
import json
import psycopg2
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

# guarda las categorias
def saveCategories(dbParams):
	file_name = "categories.json"
	categories = None
	with open(file_name) as data_file:    
		categories = json.load(data_file)

	query = 'INSERT INTO "search_category"(name) VALUES '
	params = []
	for category in categories:
		query = query + '(%s),'
		params.append(category["name"])

	query = query[:-1]
	result = executeInsert(dbParams,query,params)
	if result==None:
		print "Datos guardados"
	else:
		print result

# crea el categories_string a partir 
# de una lista de categorias
def getCategoriesString(categories):
	categories_string = ""
	for category in categories:
		categories_string += category + " "

	categories_string = categories_string[:-1]
	return categories_string

# guarda las variables
def saveVariables(dbParams):
	file_name = "variables.json"
	variables = None
	with open(file_name) as data_file:
		variables = json.load(data_file)

	query = 'INSERT INTO "timeSeries_variable"("name","unit","symbol","datatype",'
	query = query + '"categories_string") VALUES '
	params = []
	for variable in variables:
		query = query + '(%s,%s,%s,%s,%s),'
		params.append(variable["name"])
		params.append(variable["unit"])
		params.append(variable["symbol"])
		params.append(variable["datatype"])
		categories_string = getCategoriesString(variable["categories"])
		params.append(categories_string)

	query = query[:-1]
	result = executeInsert(dbParams,query,params)
	
	if result==None:
		print "Datos guardados"
	else:
		print result

# guarda los tipos de station
def saveStationTypes(dbParams):
	# carga los datos desde el json
	file_name = "stationTypes.json"
	stationTypes = None
	with open(file_name) as data_file:
		stationTypes = json.load(data_file)

	# lo guarda en la base de datos
	query = 'INSERT INTO "timeSeries_stationtype"("brand","model","automatic") VALUES'
	params = []
	for stationType in stationTypes:
		query = query + '(%s,%s,%s),'
		params.append(stationType["brand"])
		params.append(stationType["model"])
		params.append(stationType["automatic"])

	query = query[:-1]
	result = executeInsert(dbParams,query,params)
	
	if result==None:
		print "Tipos de estaciones guardadas"
	else:
		print result

	# recupera los tipos de estaciones
	query = 'SELECT id,brand,model FROM "timeSeries_stationtype"'
	stationTypes_db,error = executeSelect(dbParams,query,[])
	# se recuperan las variables
	query = 'SELECT id,name FROM "timeSeries_variable"'
	variables_db,error = executeSelect(dbParams,query,[])

	# se guardan los datos en la tabla intermedia typestation--variable
	query = 'INSERT INTO "timeSeries_stationtype_variables"("stationtype_id","variable_id") VALUES'
	params = []
	for stationType in stationTypes:
		# se buscar el id de la stationType
		id_station = None
		for stationType_db in stationTypes_db:
			if(stationType_db[1]==stationType["brand"] and 
				stationType_db[2]==stationType["model"]):
				id_station = stationType_db[0]

		variables = stationType["variables"]
		for variable in variables:
			# se busca el id de la variable
			id_variable = None
			for variable_db in variables_db:
				if(variable_db[1]==variable):
					id_variable = variable_db[0]

			query = query + "(%s,%s),"
			params.append(id_station)
			params.append(id_variable)

	query = query[:-1]
	result = executeInsert(dbParams,query,params)
	if result==None:
		print "Se guardaron las relaciones stationType -< variable"
	else:
		print result

# guarda las estaciones
def saveStations(dbParams):
	file_name = "stations.json"
	stations = None
	with open(file_name) as data_file:
		stations = json.load(data_file)

	# se recuperan los tipos de estacion
	query = 'SELECT id,brand FROM "timeSeries_stationtype"'
	stationTypes,error = executeSelect(dbParams,query,[])

	query = 'INSERT INTO "timeSeries_station"("serialNum","location","active",'
	query = query + '"frequency","token","stationType_id") VALUES '
	params = []
	for station in stations:
		params.append(station["serialNum"])
		location = station["location"]
		parts = location.split(",")
		latitude = parts[0]
		longitude = parts[1]
		params.append(station["active"])
		params.append(station.get("frequency",None))
		params.append(station.get("token",None))
		str_location = "ST_GeomFromText(\'POINT(%s %s)\',4326)"%(longitude,latitude)
		stationtype_id = None
		for stationType in stationTypes:
			if(stationType[1]==station["stationType"]):
				stationtype_id = stationType[0]

		params.append(stationtype_id)
		query = query + '(%s,'+str_location+',%s,%s,%s,%s),'

	query = query[:-1]
	result = executeInsert(dbParams,query,params)
	if result==None:
		print "Datos guardados"
	else:
		print result


if __name__ == "__main__":
	file_name = "../../dbparams.json"
	dbParams = None
	with open(file_name) as data_file:
		dbParams = json.load(data_file)

	print "Los parametros de la base de datos: ",dbParams
	print "Guardando categorias..."
	saveCategories(dbParams)
	print "Guardando Variables..."
	saveVariables(dbParams)
	print "Guardando Tipos de estaciones..."
	saveStationTypes(dbParams)
	print "Guardando Estaciones ..."
	saveStations(dbParams)


