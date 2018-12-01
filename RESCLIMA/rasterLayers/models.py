# -*- coding: utf-8 -*-
from django.contrib.gis.db import models
from layer.models import Layer

class RasterLayer(Layer):
	file_path = models.CharField(max_length=255)
	file_name = models.CharField(max_length=50)
	file_format = models.CharField(max_length=10)
	numBands = models.IntegerField(default=1)

