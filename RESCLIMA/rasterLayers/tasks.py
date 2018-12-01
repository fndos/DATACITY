# -*- encoding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
import datetime
from osgeo import gdal
from celery import shared_task, current_task
from .utils import getBBox
from .models import RasterLayer
from main.models import User

@shared_task
def import_raster_layer(rasterlayer_params):
	# se obtienen los parametros de la capa
	path = rasterlayer_params["path"]
	fileName = rasterlayer_params["fileName"]
	fullName = rasterlayer_params["fullName"]
	fullName_proj = rasterlayer_params["fullName_proj"]
	extension = rasterlayer_params["extension"]
	title = rasterlayer_params["title"]
	abstract = rasterlayer_params["abstract"]
	# fecha como string
	date_str = rasterlayer_params["date_str"]
	# fecha como objeto datetime
	data_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
	categories_string = rasterlayer_params["categories_string"]
	owner_id = rasterlayer_params["owner"]
	owner = User.objects.get(id=owner_id)

	'''
	Diccionario con el resultado de la operacion.
	Este diccionario  estara  dentro de un objeto 
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

	# se actualiza el progreso 5%
	result["error"]=None
	result["percent"]=5
	current_task.update_state(state='PROGRESS',meta=result)

	# se reproyecta la capa a EPSG:3857
	datasource = gdal.Warp(fullName_proj,fullName, dstSRS="EPSG:3857")
	if datasource==None:
		# se borra todo
		os.remove(fullName)
		if os.path.exists(fullName_proj):
			os.remove(fullName_proj)
		# se actualiza con un error
		result["error"]="Error al proyectar a EPSG:3857"
		current_task.update_state(state='FAILURE',meta=result)
		return result

	# se actualiza el progreso
	result["error"]=None
	result["percent"]=20
	current_task.update_state(state='PROGRESS',meta=result)

	numBands = datasource.RasterCount
	srs_wkt = datasource.GetProjection()

	# se actualiza el progreso
	result["error"]=None
	result["percent"]=30
	current_task.update_state(state='PROGRESS',meta=result)

	# se obtiene el bbox
	bbox = getBBox(datasource)
	if bbox==None:
		# se borra todo
		os.remove(fullName)
		os.remove(fullName_proj)
		# se actualiza con un error
		result["error"]="Esta capa no esta geo-referenciada"
		current_task.update_state(state='FAILURE',meta=result)
		return result

	# se actualiza el progreso
	result["error"]=None
	result["percent"]=50
	current_task.update_state(state='PROGRESS',meta=result)


	# se guarda en la base de datos
	rasterlayer = RasterLayer()
	rasterlayer.file_path = path
	rasterlayer.file_name = fileName
	rasterlayer.file_format = extension
	# proyected
	rasterlayer.title = title
	rasterlayer.abstract = abstract
	rasterlayer.data_date = data_date
	rasterlayer.categories_string = categories_string
	rasterlayer.srs_wkt = srs_wkt
	rasterlayer.numBands = numBands
	rasterlayer.bbox = bbox
	rasterlayer.type = "raster"
	rasterlayer.owner = owner
	rasterlayer.save()
	
	result["error"]=None
	result["percent"]=100
	current_task.update_state(state='PROGRESS',meta=result)
	return result

