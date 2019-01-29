import csv
from .models import Data_logistica

def copy_csv_gauging(ROUTE)
	data = csv.DictReader(open(ROUTE))
	for row in data:
	    Data_logistica.objects.create(id_term=row['id_term'],
										value=row['value'],
										vehicle_type=row['vehicle_type'],
										movement=row['movement'],
										id_aforo=row['id_aforo'])