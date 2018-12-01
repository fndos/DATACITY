# -*- encoding: utf-8 -*-
import os
from os.path import join
from RESCLIMA import settings
import time
import datetime
import shutil
from tasks import import_raster_layer

'''
Funcion  para  importar  los datos de
una capa vectorial. Recibe un request
de django
(django.http.request.HttpRequest).
Valida y guarda el archivo geotiff.
Ejecuta   una  tarea  de  Celery  que
guardara   los   datos  en la base de
datos.
'''
def import_data(request):
	'''
	result={}: Diccionario con el resultado
	de la operacion. El diccionario tiene los
	siguientes keys:
	{
		"error": es un string con mensaje de error
				 o None si no hay error,
		"task_id": string con el id de la tarea de Celery.
				   Si hay error el diccionario no tendra
				   este key
	}
	'''
	result = {}
	# se obtiene las variables del post
	list_files = request.FILES.getlist('import_file')
	title = request.POST["title"]
	abstract = request.POST["abstract"]
	date_str = request.POST["data_date"]
	categories_string = request.POST["categories_string"]
	owner = request.user.id

	if (len(list_files)!=1):
		result["error"]="Se debe subir un solo archivo"
		return result

	ftemp = list_files[0]
	parts = os.path.splitext(ftemp.name)
	# se obtiene el nombre y la extension del archivo
	fileName = parts[0]
	extension = parts[1]
	# se obtiene un timestamp
	ts = time.time()
	timestamp_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
	# se genera un nuevo nombre para el archivo
	fileName = fileName + "-" + timestamp_str + extension
	path = settings.RASTER_FILES_PATH
	fullName = join(path,fileName)
	# se codifica a utf-8 el nombre del archivo
	fullName = fullName.encode('utf-8')
	# se guarda el archivo

	# si el objeto tiene el atributo temporary_file_path
	# ya esta en el disco duro
	if (hasattr(ftemp,'temporary_file_path')):
		ftemp_path = ftemp.temporary_file_path()
		# mueve el archivo
		shutil.move(ftemp_path,fullName)
	else:
		# el archivo esta en memoria y se debe
		# escribir en el disco
		f = open(fullName,'w')
		for chunk in ftemp.chunks():
			f.write(chunk)
		f.close()

	# se crea un path para la capa reproyectada
	# el nuevo archivo se llamara fullName-proj.extension

	# se transforma el str a un unicode
	# para crear el nuevo nombre
	fullName_u = fullName.decode('utf-8')
	fullName_proj = fullName_u.replace(extension,"-proj"+extension)
	# se lo tranforma el nuevo unicode a str
	fullName_proj = fullName_proj.encode('utf-8')
	# se ejecuta la tarea en Celery
	rasterlayer_params = {}
	rasterlayer_params["path"] = path
	rasterlayer_params["fileName"] = fileName
	rasterlayer_params["fullName"] = fullName
	rasterlayer_params["fullName_proj"] = fullName_proj
	rasterlayer_params["extension"] = extension
	rasterlayer_params["title"] = title
	rasterlayer_params["abstract"] = abstract
	rasterlayer_params["date_str"] = date_str
	rasterlayer_params["categories_string"] = categories_string
	rasterlayer_params["owner"] = owner

	task = import_raster_layer.delay(rasterlayer_params)

	# retorna el id del task
	result["error"] = None
	result["task_id"] = task.id
	return result
