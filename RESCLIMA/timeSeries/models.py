from django.db import models
from django.contrib.gis.db import models
from fields import JSONField
from django.utils import timezone
from search.models import FilterSearchTable

class Variable(FilterSearchTable):
	name = models.CharField(max_length=50,unique=True)
	unit = models.CharField(max_length=50)
	symbol = models.CharField(max_length=10)
	datatype = models.CharField(max_length=20)

	def __unicode__(self):
		return "%s %s %s" % (self.name,self.unit,self.symbol)
	def __str__(self):
		return "%s %s %s" % (self.name,self.unit,self.symbol)

	class Meta:
		verbose_name = "Variable"
		verbose_name_plural = "Variables"

class StationType(models.Model):
	brand = models.CharField(max_length=30)
	model = models.CharField(max_length=30)
	automatic = models.BooleanField(default=False)
	variables = models.ManyToManyField(Variable, blank = True)

	def __unicode__(self):
		return "%s-%s" % (self.brand,self.model)

	def __str__(self):
		return "%s-%s" % (self.brand,self.model)

	class Meta:
		verbose_name = "Tipo de estacion"
		verbose_name_plural = "Tipo de estaciones"

class Station(models.Model):
	serialNum = models.CharField(max_length=30)
	location = models.PointField(srid=4326)
	active = models.BooleanField()
	stationType = models.ForeignKey(StationType, on_delete=models.CASCADE)
	frequency = models.FloatField(blank=True,null=True)
	token = models.CharField(max_length=30, blank=True, null=True)

	def __unicode__(self):
		return "%s %s %s %s" % (self.serialNum,self.location,self.active,self.stationType)

	def __str__(self):
		return "%s %s %s %s" % (self.serialNum,self.location,self.active,self.stationType)

	class Meta:
		verbose_name = "Estation"
		verbose_name_plural = "Estationes"


class Provider(models.Model):
	name = models.CharField(max_length = 120, default = "Proveedor")
	info = JSONField(default = dict)

	def __unicode__(self):
		return "%s" % (self.info)

	def __str__(self):
		return "%s" % (self.info)

	class Meta:
		verbose_name = "Proveedor"
		verbose_name_plural = "Proveedores"


class Measurement(models.Model):
	id_m = models.AutoField(primary_key=True)
	ts = models.DateTimeField(default=timezone.now)
	idStation = models.ForeignKey(Station, null=True, on_delete=models.CASCADE)
	idProvider = models.ForeignKey(Provider, null=True, on_delete=models.CASCADE, blank=True)
	readings = JSONField(default = dict)

	def __unicode__(self):
		return "%s %s %s %s" % (self.idStation,self.idProvider,self.ts,self.readings)
	def __str__(self):
		return "%s %s %s %s" % (self.idStation,self.idProvider,self.ts,self.readings)

	class Meta:
		verbose_name = "Measurement"
		verbose_name_plural = "Measurements"


