# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.db import connections
from django.db.models import Count
from django.http import JsonResponse, HttpResponse

from .models import *

# Create your views here.
def home(request):
    return render(request, 'visualization/home.html')

# Funcion que utiliza django filters para realizar query a la DB
# Tomada como ejemplo, para crear JsonResponse
def sample_count_by_month(request):
    data = Sample.objects.all() \
        .extra(select={'month': connections[Sample.objects.db].ops.date_trunc_sql('month', 'date')}) \
        .values('month') \
        .annotate(count_items=Count('id'))
    print(type(data))
    return JsonResponse(list(data), safe=False)

# Funcion retorna un JSON con la data que corresponde al tipo de grafico
def get_graph_data(request, value):
    query_set = Graph.objects.filter(graph_type=value) # Se debe aplicar más filtros
    for graph in query_set:
        data = graph.data
    return JsonResponse(data, safe=False)

# Funcion que renderiza el template segun el tipo de grafico
def display_graph(request, value):
    if int(value) == 1:
        return render(request, 'visualization/tree_map.html')
    elif int(value) == 2:
        return render(request, 'visualization/bar_chart.html')
    elif int(value) == 3:
        return render(request, 'visualization/donut_chart.html')
    elif int(value) == 4:
        return render(request, 'visualization/bubble_chart.html')
    else:
        return HttpResponse("No hay visualizaciones que mostrar")

# Funcion para la creacion de un grafico estadistico especifico
# Deberia recibir tipo de grafico, estilo, data y producto al que pertenece
# Crea la entrada del grafico en la base de datos
def create_graph(request):
    pass

# Funcion para la creacion de un producto
# Deberia recibir el/los clientes al que va destinado el producto y el nombre del producto
def create_product(request):
	pass
