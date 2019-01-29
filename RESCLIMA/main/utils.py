# -*- encoding: utf-8 -*-
import csv
from simulation.models import Logistica

def copy_csv_gauging(path, user):
	data = csv.DictReader(path)
	for row in data:
		Logistica.objects.create(id_term=row['id_term'],
								 value=row['value'],
								 vehicle_type=row['vehicle_type'],
								 movement=row['movement'],
								 id_gauging=row['id_gauging'],
								 user=user)
