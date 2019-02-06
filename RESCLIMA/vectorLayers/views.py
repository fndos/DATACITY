from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseNotFound, JsonResponse
from django.http import HttpResponseRedirect
from models import VectorLayer
from search.models import Category
from style.models import Style
from style.utils import transformSLD
import importer, exporter
from RESCLIMA import settings
import datetime
import time
import json
import utils
from os.path import join
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

limit = 10
@login_required(login_url='noAccess')
def list_vectorlayers(request):
	user = request.user
	user = user.id
	layers = VectorLayer.objects.filter(owner=user).order_by("upload_date")
	page = request.GET.get('page', 1)
	paginator = Paginator(layers, limit)
	try:
		vectorlayers = paginator.page(page)
	except PageNotAnInteger:
		vectorlayers = paginator.page(1)
	except EmptyPage:
		vectorlayers = paginator.page(paginator.num_pages)
	return render(request,"list_vectorlayers.html",{'vectorlayers':vectorlayers})

@login_required(login_url='noAccess')
def import_shapefile(request):
	if request.method == "GET":
		categories = Category.objects.all();
		return render(request, "import_shapefile.html",{'categories':categories});
	elif request.method == "POST":
		result = {}
		try:
			# se ejecuta la tarea de Celery
			result = importer.import_data(request)
			return HttpResponse(json.dumps(result),content_type='application/json')
		except Exception as e:
			result["error"]=str(e);
			return HttpResponse(json.dumps(result),content_type='application/json')

def export_shapefile(request, vectorlayer_id):
	try:
		vectorlayer = VectorLayer.objects.get(id=vectorlayer_id)
	except VectorLayer.DoesNotExist:
		return HttpResponseNotFound()
	return exporter.export_shapefile(vectorlayer)

def export_geojson(request, vectorlayer_id):
	try:
		vectorlayer = VectorLayer.objects.get(id=vectorlayer_id)
	except VectorLayer.DoesNotExist:
		return HttpResponseNotFound()
	geojson = exporter.export_geojson(vectorlayer)
	return HttpResponse(geojson)

def updateVectorLayer(vectorlayer,request):
	try:
		title = request.POST["title"]
		abstract = request.POST["abstract"]
		date_str = request.POST["data_date"] # fecha como string
		# fecha como objeto datetime
		data_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
		categories_string = request.POST["categories_string"]

		# se actualiza la capa
		vectorlayer.title = title;
		vectorlayer.abstract = abstract;
		vectorlayer.data_date = data_date;
		vectorlayer.categories_string = categories_string;
		vectorlayer.save()
	except Exception as e:
		return "Error " + str(e)

@login_required(login_url='noAccess')
def edit_vectorlayer(request,vectorlayer_id):
	try:
		vectorlayer = VectorLayer.objects.get(id=vectorlayer_id)
	except VectorLayer.DoesNotExist:
		return HttpResponseNotFound()
	if request.method == "GET":
		categories = Category.objects.all();
		params = {"vectorlayer":vectorlayer,"categories":categories}
		return render(request,"update_vectorlayer.html",params)

	elif request.method == "POST":
		err_msg = updateVectorLayer(vectorlayer,request)
		if(err_msg==None):
			return HttpResponseRedirect("/vector")
		else:
			categories = Category.objects.all();
			params = {"vectorlayer":vectorlayer,
					  "err_msg":err_msg,
					  "categories":categories}
			return render(request,"update_vectorlayer.html",params)

@login_required(login_url='noAccess')
def delete_vectorLayer(request,vectorlayer_id):
	try:
		vectorlayer = VectorLayer.objects.get(id=vectorlayer_id)
		vectorlayer.delete()
		return redirect('vector_list')
	except VectorLayer.DoesNotExist:
		return HttpResponseNotFound()

# Styles

def importStyle(request,vectorlayer):
	try:
		title = request.POST["title"]

		path = settings.STYLE_FILES_PATH;

		ts = time.time()
		timestamp_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
		fileName = "style_"+str(vectorlayer.id)+"_"+timestamp_str + ".sld"

		fullName = join(path,fileName)
		f = request.FILES['file']

		sld_string = f.read();
		sld_string = transformSLD(sld_string);

		f.close();
		f = open(fullName,'w');
		f.write(sld_string);
		f.close();

		owner = vectorlayer.owner;

		style = Style(file_path=path,file_name=fileName,
		  title=title, type="shapefile",owner=owner);

		style.save()
		style.layers.add(vectorlayer)
		style.save()

	except Exception as e:
		return "Error " + str(e)

@login_required(login_url='noAccess')
def import_style(request,vectorlayer_id):
	try:
		vectorlayer = VectorLayer.objects.get(id=vectorlayer_id)
	except VectorLayer.DoesNotExist:
		return HttpResponseNotFound()

	if request.method == "GET":
		params = {"vectorlayer_id":vectorlayer_id}
		return render(request,"vectorLayers/import_style.html",params);

	if request.method == "POST":
		err_msg = importStyle(request,vectorlayer)
		if(err_msg==None):
			return HttpResponseRedirect("/vector/edit/"+vectorlayer_id)
		else:
			params = {"vectorlayer_id":vectorlayer_id,"err_msg":err_msg}
			return render(request,"vectorLayers/import_style.html",params)

@login_required(login_url='noAccess')
def delete_style(request,style_id):
	try:
		style = Style.objects.get(id=style_id)
		style.delete();
		return HttpResponse("OK");
	except Style.DoesNotExist:
		return HttpResponseNotFound()

def export_style(request,style_id):
	try:
		style = Style.objects.get(id=style_id)
		file_path = style.file_path;
		file_name = style.file_name;
		fullName = join(file_path,file_name);
		f = open(fullName,'r');
		sld = f.read()
		return HttpResponse(sld)
	except Exception as e:
		return HttpResponseNotFound()
