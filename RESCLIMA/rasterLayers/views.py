# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from os.path import join
import datetime
import time
import importer
import json
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from wsgiref.util import FileWrapper
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from RESCLIMA import settings
from models import RasterLayer
from style.models import Style
from style.utils import transformSLD,getColorMap
from search.models import Category
from main.models import User


limit = 10
@login_required(login_url='noAccess')
def list_rasterlayers(request):
	user = request.user
	user = user.id
	layers = RasterLayer.objects.filter(owner=user).order_by("upload_date")
	styles = Style.objects.filter(type="raster", owner=user)
	page = request.GET.get('page', 1)
	paginator1 = Paginator(layers, limit)
	try:
		rasterlayers = paginator1.page(page)
	except PageNotAnInteger:
		rasterlayers = paginator1.page(1)
	except EmptyPage:
		rasterlayers = paginator1.page(paginator1.num_pages)
	obj = {'rasterlayers':rasterlayers,'styles':styles}
	return render(request,"list_rasterlayers.html",obj)

@login_required(login_url='noAccess')
def import_raster(request):
	if request.method == "GET":
		categories = Category.objects.all();
		return render(request, "import_raster.html",{'categories':categories})
	elif request.method == "POST":
		result = {}
		try:
			print "se ejecuta la tarea en import_raster"
			result = importer.import_data(request)
			print "el resultado de la tarea en import_raster", result
			return HttpResponse(json.dumps(result),content_type='application/json')
		except Exception as e:
			print "El error en import_raster", e
			result["error"]=str(e);
			return HttpResponse(json.dumps(result),content_type='application/json')

def export_rasterLayer(request,rasterlayer_id):
	rasterlayer = RasterLayer.objects.get(id=rasterlayer_id)
	file_path = rasterlayer.file_path
	file_name = rasterlayer.file_name
	fullName = join(file_path,file_name)

	f = FileWrapper(open(fullName,"r"))
	response = HttpResponse(f, content_type="image/tiff")
	response['Content-Disposition'] = "attachment; filename=" + file_name
	return response

def style_legend(request,style_id):
	style = Style.objects.get(id=style_id)
	legend = getColorMap(style);
	return HttpResponse(json.dumps(legend),content_type='application/json')

def updateRasterLayer(rasterlayer,request):
	try:
		title = request.POST["title"]
		abstract = request.POST["abstract"]
		id_style = request.POST["style"]
		date_str = request.POST["data_date"] # fecha como string
		# fecha como objeto datetime
		data_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
		categories_string = request.POST["categories_string"]

		rasterlayer.title = title
		rasterlayer.abstract = abstract
		rasterlayer.data_date = data_date
		rasterlayer.categories_string = categories_string
		rasterlayer.save()

		# se actualiza el estilo
		if id_style != "null":
			style = Style.objects.get(id=id_style)
			style.layers.add(rasterlayer)
			style.save()
		else:
			rasterlayer.style_set.clear()
	except Exception as e:
		return "Error " + str(e)

@login_required(login_url='noAccess')
def edit_raster(request, rasterlayer_id):
	user = request.user
	user = user.id
	try:
		rasterlayer = RasterLayer.objects.get(id=rasterlayer_id)
	except RasterLayer.DoesNotExist:
		return HttpResponseNotFound()

	# se obtienen los estilos
	styles = Style.objects.filter(type="raster", owner=user)
	# se obtiene el estilo de la capa
	layer_styles = Style.objects.filter(layers__id=rasterlayer_id)
	layer_style_id = None
	# si se encontro un estilo
	if layer_styles.count()==1:
		layer_style = layer_styles[0]
		# se recupera el id de ese estilo
		layer_style_id = layer_style.id

	# se obtienen las categorias
	categories = Category.objects.all();

	if request.method == "GET":
		params = {"rasterlayer":rasterlayer,
				  "styles":styles,
				  "layer_style_id":layer_style_id,
				  "categories":categories}
		return render(request,"update_rasterlayer.html",params)

	elif request.method == "POST":
		err_msg = updateRasterLayer(rasterlayer,request)
		if(err_msg==None):
			return HttpResponseRedirect("/raster")
		else:
			params = {"rasterlayer":rasterlayer,
					  "styles":styles,
					  "layer_style_id":layer_style_id,
					  "categories":categories,
					  "err_msg":err_msg}
			return render(request,"update_rasterlayer.html",params)

@login_required(login_url='noAccess')
def delete_rasterLayer(request,rasterlayer_id):
	try:
		rasterlayer = RasterLayer.objects.get(id=rasterlayer_id)
		file_path = rasterlayer.file_path
		file_name = rasterlayer.file_name
		fullName = join(file_path,file_name)
		os.remove(fullName)
		rasterlayer.delete()
		return HttpResponseRedirect("/raster")
	except RasterLayer.DoesNotExist:
		return HttpResponseNotFound()

# Styles
def importStyle(request):
	try:
		title = request.POST["title"]

		path = settings.STYLE_FILES_PATH;

		ts = time.time()
		timestamp_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
		fileName = "style_" + timestamp_str + ".sld"

		fullName = join(path,fileName)
		f = request.FILES['file']

		sld_string = f.read();
		sld_string = transformSLD(sld_string);

		f.close();
		f = open(fullName,'w');
		f.write(sld_string);
		f.close();

		user = request.user
		user = user.id
		owner = User.objects.get(id=user)
		style = Style(file_path=path,file_name=fileName,
		  title=title, type="raster", owner=owner);
		style.save()
	except Exception as e:
		return "Error " + str(e)

@login_required(login_url='noAccess')
def import_style(request):

	if request.method == "GET":
		return render(request,"rasterLayers/import_style.html");

	if request.method == "POST":
		err_msg = importStyle(request)
		if(err_msg==None):
			return HttpResponseRedirect("/raster")
		else:
			params = {"err_msg":err_msg}
			return render(request,"rasterLayers/import_style.html",params)

@login_required(login_url='noAccess')
def delete_style(request,style_id):
	try:
		style = Style.objects.get(id=style_id)
		file_path = style.file_path;
		file_name = style.file_name;
		fullName = join(file_path,file_name)
		os.remove(fullName)
		style.delete()
		return HttpResponseRedirect("/raster")
	except Style.DoesNotExist:
		return HttpResponseNotFound()

def export_style(request,style_id):
	try:
		style = Style.objects.get(id=style_id)
		file_path = style.file_path
		file_name = style.file_name
		fullName = join(file_path,file_name)
		f = open(fullName,'r')
		sld = f.read()
		return HttpResponse(sld)
	except Exception as e:
		return HttpResponseNotFound()
