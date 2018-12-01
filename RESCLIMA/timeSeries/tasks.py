# -*- encoding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from datetime import datetime
from dateutil.parser import parse
from timeSeries.models import Variable,Station,Measurement
from timeSeries.utils import *
import os
import commands
from celery import shared_task, current_task


'''
Funcion que recupera  el  encoding de un
archivo. Si no lo encuentra retorna None
'''
def getFileEncoding(fileName):
	command = "file -i " + fileName
	result = commands.getstatusoutput(command)
	if(result[0]!=0):
		return None

	text = result[1]
	index = text.find("charset=")
	if index==-1:
		return None

	index = index + 8
	encoding = text[index:]
	encoding = encoding.strip()
	if(encoding==''):
		return False

	return encoding

'''
Obtiene las columnas de una linea del csv,
la cual tiene este formato:
"co1","col2, puede tener comas, ",col3 sin comillas,"col4"
Retorna un arreglo con las columnas
'''
def getColumns(line):
	columns = []
	column = ""
	ignoreComas = False
	for c in line:
		if(c=="," and not(ignoreComas)):
			columns.append(column)
			column = ""
			continue
		
		if(c=='"' and not(ignoreComas)):
			ignoreComas = True
			continue
		
		if(c=='"' and ignoreComas):
			ignoreComas = False
			continue

		column = column + c

	columns.append(column)
	return columns

'''
parseHobo(file)
Task de celery que lee un archivo
que proviene de las estaciones 
meteorologicas de tipo HOBO-MX2300
y se encarga de guardar los datos 
en la base de datos.
'''

# parsea una medicion segun su tipo de dato
def parseMeasure(measure,datatype):

	if(datatype=="float"):
		measure = measure.replace(",",".")
		return float(measure)
	elif(datatype=="string"):
		return measure;
	else:
		return None;

@shared_task
def parseHOBOFile(hoboParams):
	# se obtiene el nombre del archivo
	fileName = hoboParams["fileName"]
	'''
	Diccionario con el resultado de la operacion.
	Este  diccionario  estara dentro de un objeto 
	celery.result.AsyncResult
	result = {
				"error": string  con  mensaje de error, 
						 si no hay error, esta clave no 
						 existira o sera None
				"percent": porcentaje de progreso de la
						   operacion
			}
	'''
	result = {}
	# abre el archivo
	f = None
	if os.path.isfile(fileName):
		f = open(fileName,'r')
	else:
		result["error"]="Error, se perdio el archivo"+fileName;
		current_task.update_state(state='FAILURE',meta=result)
		return result

	'''
	se comprueba  el numero de  lineas del 
	archivo se requieren al menos 3 lineas
	1era linea: contiene el numero de serie de la estacion
	2da linea: contiene el header del csv
	3ra linea: datos
	'''
	num_lines = count_file_lines(f)
	if (num_lines<4):
		result["error"]="Error: archivo sin datos";
		current_task.update_state(state='FAILURE',meta=result)
		return result

	# formato de la fecha
	datetime_format = "%Y-%m-%d %H:%M:%S"
	# time zone de las fechas de los datos (ej.: UTC,GMT+2,GMT-4,etc)
	local_tz_str = None;
	# numero de serie de la estacion
	serialNum = None;
	# objeto con datos de la estacion
	station = None;

	# actualiza el porcentaje de avance de la tarea: 5%
	result["error"]=None
	result["percent"]=5
	current_task.update_state(state='PROGRESS',meta=result)


	percent_cont = 0
	encoding = getFileEncoding(fileName)

	# si no se pudo determinar el encoding
	# del archivo, se prueba con utf-8
	if(encoding==None):
		encoding = 'utf-8'


	# se obtienen las variables de la base de datos
	temp = Variable.objects.get(name=u"Temperatura")
	rh = Variable.objects.get(name=u"Humedad relativa")
	variables = [temp,rh]

	# se itera el archivo
	for i,line in enumerate(f,1):
		try:
			line = line.decode(encoding)
		except Exception as e:
			# se borra el archivo
			os.remove(fileName)
			result["error"]="Error: el encoding "+encoding + " del archivo no es correcto"
			current_task.update_state(state='FAILURE',meta=result)
			return result

		# si se lee la primera linea del archivo
		# se recupera el numero serial de la estacion
		if(i==1):
			# la primera linea contiene "Serial Number: string --"
			# string es el  numero serial  de la estacion
			parts = line.split(":")
			if (len(parts)==2):
				serialNum = parts[1]
				# se eliminan caracteres en blanco
				serialNum = serialNum.strip(' \t\n\r')
				# se remueven los tres ultimos caracteres (" --")
				serialNum = serialNum[:-3]
			else:
				# se borra el archivo
				os.remove(fileName)
				result["error"]="Error: no se especifica el numero de serie de la estacion"
				current_task.update_state(state='FAILURE',meta=result)
				return result

			# se valida que la estacion existe en la base de datos
			results=Station.objects.filter(serialNum=serialNum);
			if(results.count()!=1):
				# se borra el archivo
				os.remove(fileName)
				result["error"]="Error: no se encontro la estacion "+serialNum
				current_task.update_state(state='FAILURE',meta=result)
				return result
			else:
				station = results[0]

			# se comprueba que el tipo de stacion sea HOBO-MX2300
			typestation = str(station.stationType)
			if(typestation!="HOBO-MX2300"):
				# se borra el archivo
				os.remove(fileName)
				result["error"]="Error: la estacion debe ser de tipo HOBO-MX2300"
				current_task.update_state(state='FAILURE',meta=result)
				return result


			result["percent"]=10
			current_task.update_state(state='PROGRESS',meta=result)

			continue;

		# se ignora la linea 2, porque es vacia
		if(i==2):
			continue;

		# la tercera linea contiene los headers
		if(i==3):
			headers = getColumns(line);
			if len(headers)!=14:
				# se borra el archivo
				os.remove(fileName)
				msg = "Error: el archivo debe tener ocho columnas, "
				ms = msg + "se tienen "+str(len(headers)) + " columnas"
				result["error"]=msg
				current_task.update_state(state='FAILURE',meta=result)
				return result

			# se obtiene la informacion del timezone
			# el string debe ser parseado para obtener el ofset 
			# en horas
			header_date = headers[0]
			index = header_date.find("GMT")
			time_zone_str = header_date[index:].strip(' \t\n\r')
			offset_str = time_zone_str[4:7]
			offset = int(offset_str)
			# se crea el string del timezone
			if(offset<0):
				local_tz_str = "Etc/GMT-" + str(abs(offset));
			elif(offset >0):
				local_tz_str = "Etc/GMT+" + str(abs(offset));
			else:
				local_tz_str="UTC";

			# se actualiza el progreso
			result["percent"]=20
			current_task.update_state(state='PROGRESS',meta=result)

			continue;

		# si la linea es mayor que la 3
		# se obtienen las mediciones
		measures = getColumns(line)
		if(len(measures)!=14):
			# se borra el archivo
			os.remove(fileName)
			result["error"]="Error: falta una columna en la linea "+str(i)
			current_task.update_state(state='FAILURE',meta=result)
			return result
		# se recupera la fecha hora de la primera columna
		datetime_str = measures[0]
		try:
			# se crea un objeto datetime desde el string y el formato
			dt = datetime.strptime(datetime_str,datetime_format);
			# se transforma la fecha del time zone local a UTC
			dt = transformToUTC(dt,local_tz_str);
		except Exception as e:
			# se borra el archivo
			os.remove(fileName)
			result["error"]="Error: la fecha "+datetime_str+" no es correcta"+str(e)
			current_task.update_state(state='FAILURE',meta=result)
			return result

		# en la columna 1 esta temperatura y en la 6, la humedad relativa
		variables_index = [1,6]
		measures_dict = {}
		for i,j in enumerate(variables_index):
			measure = measures[j]
			measure = measure.strip(' \t\n\r')
			variable = variables[i]

			if measure == "":
				continue;

			idVariable = variable.id;
			datatype = variable.datatype;
			measure = parseMeasure(measure,datatype);
			# se agrega al diccionario de variables y
			# mediciones
			measures_dict[idVariable]=measure;
		
		# se guardan las mediciones
		saveMeasurements(station,None,measures_dict, dt);

		# se actualiza el porcentaje de progreso de 30 a 90
		percent_cont = percent_cont%10
		percent_cont += 1
		# cada 50 lineas actualiza el progreso
		if(percent_cont==0):
			percent = 30 + (float(i)/num_lines)*75
			result["error"]=None
			result["percent"]=percent
			current_task.update_state(state='PROGRESS',meta=result)
		

	# se completa la tarea
	result["percent"]=100		
	return result



