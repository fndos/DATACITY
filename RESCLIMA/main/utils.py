# -*- encoding: utf-8 -*-
import csv
from .models import *

def copy_csv_logistica(path, user):
	data = csv.DictReader(path)
	for row in data:
		Logistica.objects.create(id_term=row['id_term'],
								 value=row['value'],
								 vehicle_type=row['vehicle_type'],
								 movement=row['movement'],
								 id_gauging=row['id_gauging'],
								 date=row['date'],
								 user=user)

def copy_csv_clima(path, user):
	data = csv.DictReader(path)
	for row in data:
		Clima.objects.create(date=row['date'],
								 tmin=row['tmin'],
								 tmax=row['tmax'],
								 rr=row['rr'],
								 oni=row['oni'],
								 user=user)

def copy_csv_censo(path, user):
	data = csv.DictReader(path)
	for row in data:
		Censo.objects.create(year=row['year'],
								 man=row['man'],
								 woman=row['woman'],
								 total_pob=row['total_pob'],
								 lettered=row['lettered'],
								 unlettered=row['unlettered'],
								 housing=row['housing'],
								 user=user)
