# -*- encoding: utf-8 -*-

from timeSeries.models import Variable,Station,Measurement,Provider
from django.db import connection
import pytz
import json

# cuenta las lineas de un archivo
def count_file_lines(f):
	count_lines = len(f.readlines())
	f.seek(0)
	return count_lines


def transformToUTC(dt,local_tz_str):
	if(local_tz_str=="UTC"):
		return dt
	local_tz = pytz.timezone (local_tz_str);
	dt_with_tz = local_tz.localize(dt, is_dst=None)
	dt_in_utc = dt_with_tz.astimezone(pytz.utc)
	return dt_in_utc;

# guarda una medicion en la base de datos
def saveMeasurements(station,id_provider,measurements_dict,date_time):

	measurements=json.dumps(measurements_dict);
	idStation = station.id

	qs = "SELECT InsertMeasurements(%s::integer,%s::timestamp,%s::json)"
	params = [idStation,date_time,measurements]
	with connection.cursor() as cursor:
		cursor.execute(qs, params)
