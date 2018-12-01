from django.db import models
from layer.models import Layer
from main.models import User

class Style(models.Model):
	file_path = models.CharField(max_length=255)
	file_name = models.CharField(max_length=50)
	title = models.CharField(max_length=50)
	type = models.CharField(max_length=10)
	layers = models.ManyToManyField(Layer)
	owner = models.ForeignKey(User)
