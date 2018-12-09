# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.db import connections
from django.db.models import Count
from django.http import JsonResponse

from .models import Sample

# Create your views here.
def sample(request):
    return render(request, 'visualization/sample.html')

def sample_count_by_month(request):
    data = Sample.objects.all() \
        .extra(select={'month': connections[Sample.objects.db].ops.date_trunc_sql('month', 'date')}) \
        .values('month') \
        .annotate(count_items=Count('id'))
    return JsonResponse(list(data), safe=False)
#Funcion para la creacion de un grafico estadistico especifico
#Deberia recibir tipo de grafico, estilo, data y producto al que pertenece
#Crea la entrada del grafico en la base de datos
def create_graph(request):
	pass
#Funcion para la creacion de un producto
#Deberia recibir el/los clientes al que va destinado el producto y el nombre del producto
def create_product(request):
	pass
