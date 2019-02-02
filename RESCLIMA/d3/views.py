# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.db import connections, connection
from django.http import JsonResponse, HttpResponse

from timeSeries.models import Measurement

import json

# Create your views here.

# Funcion que utiliza django filters para realizar query a la DB
# Tomada como ejemplo, para crear JsonResponse
# Eliminar
def test(request):

	select_stm = 'SELECT v."id", v."name", array_agg(s.id) as stations, count(*) OVER() AS full_count '
	from_stm = 'FROM "timeSeries_variable" as v, "timeSeries_stationtype" as st, "timeSeries_station" as s, "timeSeries_stationtype_variables" as st_v '
	# JOIN entre station y stationType
	where_stm = 'WHERE s."stationType_id" = st."id" AND '
	# JOIN entre stationType y la tabla intermedia (station_type_variables)
	where_stm = where_stm + 'st."id" = st_v."stationtype_id" AND '
	# JOIN entre tabla intermedia (station_type_variables) y variable
	where_stm = where_stm + 'st_v."variable_id" = v."id" '

	qs = select_stm + from_stm + where_stm
	qs = qs + 'GROUP BY  v.id '

	params = []
	series = []
	full_count = 0;
	with connection.cursor() as cursor:
		cursor.execute(qs, params)
		rows = cursor.fetchall()
		for row in rows:
			serie = {}
			serie["variable_id"]=row[0]
			serie["variable_name"]=row[1]
			serie["stations"] = row[2]
			serie["selected"] = False
			full_count=row[3]
			series.append(serie);

	print series
	return JsonResponse({"series":series,"full_count":full_count})
