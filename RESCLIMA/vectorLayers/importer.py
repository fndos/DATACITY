# -*- encoding: utf-8 -*-
import os
import time, datetime
import shutil
from tasks import import_vector_layer
from RESCLIMA import settings

def createTempFolder():
	t = time.time()
	ts = datetime.datetime.fromtimestamp(t)
	timestamp_str = ts.strftime('%Y-%m-%d-%H-%M-%S')
	folderName = "layer" + timestamp_str
	fullName = os.path.join(settings.TEMPORARY_FILES_PATH,folderName)
	os.mkdir(fullName)
	return fullName

'''
Funcion para importar los datos de
un shapefile. Recibe un request de
django
(django.http.request.HttpRequest).
Valida   y  guarda  los  archivos.
Ejecuta  una tarea  de  Celery que
guardara los datos  en la  base de
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

	# se obtienen las variables del POST
	list_files = request.FILES.getlist("import_files")
	encoding  = request.POST["encoding"]
	title = request.POST["title"]
	abstract = request.POST["abstract"]
	date_str = request.POST["data_date"]
	categories_string = request.POST["categories_string"]
	# el id del user
	owner = request.user.id

	'''
	Se verifica que esten unicamente los archivos
	requeridos y que todos  deben tener  el mismo
	nombre (Este es  un  requisito  de shapefile)
	'''
	required_extensions = [".shp", ".shx", ".dbf", ".prj"]
	has_extension = {}

	for extension in required_extensions:
		has_extension[extension] = False

	filename = None;
	for f in list_files:
		# se obtiene el nombre y extension del archivo
		parts = os.path.splitext(f.name)
		fname = parts[0]
		extension = parts[1]
		# se comprueba que todos los archivos se llamen igual
		if(filename==None):
			filename = fname
		elif(filename!=fname):
			result["error"] = "Todos los archivos deben tener el mismo nombre";
			return result;

		if extension in required_extensions:
			has_extension[extension] = True;
		else:
			result["error"] = "No se admite archivo con extension " + extension;
			return result;

	# se valida que los archivos requeridos existan
	for extension in required_extensions:
		if (not(has_extension[extension])):
			result["error"] = "Archivo perdido requerido ." + extension
			return result

	# se crea una una carpeta temporal
	# para guardar los archivos
	temp_dir = createTempFolder()
	vectorlayer_name = filename + ".shp" # nombre del archivo shapefile

	for ftemp in list_files:
		'''
		Si el objeto  ftemp de tipo  UploadedFile, tiene
		el atributo: ftemp.file.name significa que ftemp
		es una instancia de TemporaryUploadedFile lo que
		siginifica  que el archivo  esta  guardado en el
		disco en un directorio temporal.
		Si ftemp no tiene el  atributo: ftemp.file.name,
		ftemp es una  instancia de InMemoryUploadedFile,
		lo que significa que los datos del archivo estan
		en memoria.
		Si los  archivos  ya  estan en el  disco, se los
		mueve hacia el directorio temporal temp_dir.
		Si los archivos estan memoria, se los escribe en
		el disco dentro del directorio temporal temp_dir
		'''

		# nueva ubicacion del archivo
		ftemp_path_dst = os.path.join(temp_dir,ftemp.name)
		# se codifica a utf-8 el nombre del archivo
		ftemp_path_dst = ftemp_path_dst.encode('utf-8')

		if (hasattr(ftemp,'temporary_file_path')):
			# el archivo ya esta en disco
			ftemp_path = ftemp.temporary_file_path()
			# mueve el archivo
			shutil.move(ftemp_path,ftemp_path_dst)
		else:
			# el archivo esta en memoria

			# se crea un archivo en el directorio temporal
			f = open(ftemp_path_dst, 'wb+')

			# se guardan los datos en el archivo
			for chunk in ftemp.chunks():
				f.write(chunk)
			f.close()

		ftemp.close()

	# se llama a la tarea de celery
	# para que se ejecute asincronicamente

	# La tarea de celery requiere un diccionario
	# con parametros
	vectorlayer_params = {}
	vectorlayer_params["temp_dir"] = temp_dir
	vectorlayer_params["vectorlayer_name"] = vectorlayer_name
	vectorlayer_params["encoding"] = encoding
	vectorlayer_params["title"] = title
	vectorlayer_params["abstract"] = abstract
	vectorlayer_params["date_str"] = date_str
	vectorlayer_params["categories_string"] = categories_string
	vectorlayer_params["owner"] = owner

	task = import_vector_layer.delay(vectorlayer_params)
	# se retorna que no hay error y el id del task
	result["error"] = None
	result["task_id"] = task.id;

	return result;
