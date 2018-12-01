import saveMeasurements
import sys
import json


if __name__ == "__main__":
	file_name = sys.argv[1]
	print(file_name)
	dbParams = None
	with open(file_name) as data_file:
		dbParams = json.load(data_file)

	print "Los parametros de la base de datos: ",dbParams
	
	stations, stationTypes = saveMeasurements.getData(dbParams)
	print "Las estaciones obtenidas", stations
	print "Los tipos de estaciones con sus variables: ", stationTypes
	print "Creando series de tiempo..."
	saveMeasurements.saveTimeSeriesDynamic(stations,stationTypes, dbParams)
