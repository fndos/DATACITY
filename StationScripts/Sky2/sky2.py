#!/usr/bin/python
# -*- encoding: utf-8 -*-
import time
import urllib2 
import json
import time
from datetime import datetime
import psycopg2
import logging
from threading import Condition, Thread
from Queue import Queue
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# Script que descarga los datos
# de las estaciones SKY2 y las guarda en 
# la base de datos

# archivos de configuracion, log y backup
configFileName = "/home/manager/RESCLIMA/dbparams.json";
logFileName = "/home/manager/RESCLIMA/StationScripts/Sky2/log.txt"
backupFileName = "/home/manager/RESCLIMA/StationScripts/Sky2/backup.txt";

# variable de condicion
# para dormir el main
cv = Condition()
# cola para escribir en el archivo
# de backup
writeQueue = Queue()

def backup(measurement):
	measurement = measurement + "\n"
	writeQueue.put(measurement)
	outFile = open(backupFileName,'a')
	while writeQueue.qsize():
		outFile.write(writeQueue.get())
	outFile.flush()
	outFile.close()

def getVariablesByNames(dbParams,variable_names):
	variables = []
	conn = None
	try:
		# se recuperan todas las variables de la base de datos
		conn = psycopg2.connect(host=dbParams["host"],
								port=dbParams["port"],
								user=dbParams["user"],
								password=dbParams["password"],
								dbname=dbParams["dbname"])
		cursor = conn.cursor()

		query = """
				SELECT v.id,v.name,v.datatype
	            FROM "timeSeries_variable" as v
	            """;
		cursor.execute(query)
		variables_db = cursor.fetchall()

		for v in variables_db:
			name = v[1].decode('utf-8')
			if v[1] in variable_names:
				variable = {}
				variable["id"] = v[0];
				variable["name"] = name;
				variable["datatype"] = v[2];
				variables.append(variable);

	except Exception as e:
		error_str = "Fallo la base de datos" + str(e);
		return None,error_str;
	finally:
		if conn:
			conn.close()

	return variables,None 

def getStations(dbParams):
	stations = []
	conn = None
	try:
		conn = psycopg2.connect(host=dbParams["host"],
								port=dbParams["port"],
								user=dbParams["user"],
								password=dbParams["password"],
								dbname=dbParams["dbname"])
		cursor = conn.cursor()

		query = """
				SELECT s.id,s.token,s.frequency
                FROM "timeSeries_station" as s,   
                "timeSeries_stationtype" as st 
                WHERE st.brand='BloomSky' and st.model='SKY2' 
                and s."stationType_id"=st.id
                """
		
		cursor.execute(query);
		results = cursor.fetchall();
		for row in results:	
			station = {}
			station["id"] = row[0];
			station["token"] = row[1];
			station["frequency"] = row[2];
			stations.append(station);

	except Exception as e:
		error_str = "Fallo la base de datos " + str(e);
		return None,error_str;
	finally:
		if conn:
			conn.close()

	return stations,None 

def getSKY2Data(token):
	try:
		url = 'https://api.bloomsky.com/api/skydata/.?unit=intl'
		request = urllib2.Request(url)
		request.add_header('Authorization', token)
		response = urllib2.urlopen(request).read()
		return response,None
	except Exception as e:
		error_str = "Error al descargar datos " + str(e)
		return None,error_str

def parseMeasurements(idStation,data,variables):
	source = json.loads(data)[0]
	readings = source['Data']
	timestamp = readings['TS']
	dt = datetime.utcfromtimestamp(timestamp)	
	timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S")


	result = {}
	for variable in variables:
		idVariable = variable["id"];
		alias = variable["alias"];
		result[idVariable] = readings[alias];

	values = json.dumps(result);
	measurement = {}
	measurement["idStation"]=idStation
	measurement["datetime"]=timestamp_str
	measurement["values"]=values
	return measurement, None

def insertMeasures(dbParams,measurements):
	conn = None
	try:
		conn = psycopg2.connect(host=dbParams["host"],
								port=dbParams["port"],
								user=dbParams["user"],
								password=dbParams["password"],
								dbname=dbParams["dbname"])
		cursor = conn.cursor()
		query = "SELECT InsertMeasurements(%s::integer,%s::timestamp,%s::json)"
		idStation = measurements["idStation"]
		timestamp_str = measurements["datetime"]
		values = measurements["values"]
		cursor.execute(query,(idStation,timestamp_str,values,));
		conn.commit()
	except Exception as e:
		error_str = "Fallo la base de datos " + str(e);
		return error_str;
	finally:
		if conn:
			conn.close()

	return None 

def dataExtraction_thread(dbParams,station,variables):
	idStation = station["id"]
	token = station["token"]
	frequency = station["frequency"]
	seconds = frequency*60
	while(True):
		time.sleep(seconds)
		data,error = getSKY2Data(token);
		if(error):
			logging.error(error)
			continue
		measurements,error = parseMeasurements(idStation,data,variables)
		if(error):
			logging.error(error)
			continue

		error = insertMeasures(dbParams,measurements) 
		if(error):
			logging.error(error)
			# intenta guardar en el backup
			m_dump = json.dumps(measurements)
			backup(m_dump);


if __name__ == "__main__":
	
	# se inicializa el logger
	logging.basicConfig(filename=logFileName,
						format='%(asctime)s %(message)s')
	logging.debug('Adaptador SKY2 inicializado')

	
	# Se otienen las credenciales de 
	# la base de datos
	dbParams = None
	with open(configFileName) as f:
		dbParams = json.load(f)


	# lista de los nombres de las variables
	variable_names = [u"Luminancia",
					  u"Temperatura",
					  u"Imagen SKY2",
					  u"Detección de lluvia",
					  u"Presión",
					  u"Indice UV"]


	variables,error = getVariablesByNames(dbParams,variable_names);
	# se les debe agregar el alias a cada variable
	variables_alias = {}
	variables_alias[u"Luminancia"]=u"Luminance"
	variables_alias[u"Temperatura"]=u"Temperature"
	variables_alias[u"Imagen SKY2"]=u"ImageURL"
	variables_alias[u"Detección de lluvia"]=u"Rain"
	variables_alias[u"Presión"]=u"Pressure"
	variables_alias[u"Indice UV"]=u"UVIndex"


	for variable in variables:
		name = variable["name"]
		alias = variables_alias[name]
		variable["alias"]=alias

	if(error):
		logging.error(error)
		exit(-1);
	
	stations,error = getStations(dbParams);

	if(error):
		logging.error(error)
		exit(-1);

	for station in stations:
		thread_ = Thread(target=dataExtraction_thread, args=(dbParams,station,variables,));
		thread_.setDaemon(True)
		thread_.start()

	cv.acquire()
	cv.wait()


