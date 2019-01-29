import csv
from .models import *******

def copy_csv_gauging(ROUTE)
	data = csv.DictReader(open(ROUTE))
	for row in data:
	    MyModel.objects.create(name=row['NAME'], number=row['NUMBER'])