# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from search.models import FilterSearchTable
from main.models import User

# Create your models here.
class Layer(FilterSearchTable):
	title = models.CharField(max_length=50,null=True)
	abstract = models.TextField(max_length=500,null=True)
	type = models.CharField(max_length=10)
	data_date = models.DateField(blank=True,null=True)
	upload_date = models.DateTimeField(auto_now_add=True)
	srs_wkt = models.TextField(max_length= 500)
	bbox = models.PolygonField(srid=4326,null=True)
	owner = models.ForeignKey(User)
