from django.contrib.gis.db import models
from RESCLIMA import settings
from os.path import join
from django.contrib.auth.models import User
from layer.models import Layer


class VectorLayer(Layer):
	filename = models.CharField(max_length= 255)
	geom_type = models.CharField(max_length= 50)
	encoding = models.CharField(max_length= 20)

class Attribute(models.Model):
	vectorlayer = models.ForeignKey(VectorLayer)
	name = models.CharField(max_length= 255)
	type = models.IntegerField()
	width = models.IntegerField()
	precision = models.IntegerField()

class Feature(models.Model):
	vectorlayer = models.ForeignKey(VectorLayer)
	geom_point = models.PointField(srid=4326,blank=True,null=True)
	geom_multipoint = models.MultiPointField(srid=4326,blank=True,null=True)
	geom_multilinestring = models.MultiLineStringField(srid=4326,blank=True,null=True)
	geom_multipolygon = models.MultiPolygonField(srid=4326,blank=True,null=True)
	geom_geometrycollection = models.GeometryCollectionField(srid=4326,blank=True,null=True)

	objects = models.GeoManager()


class AttributeValue(models.Model):
	feature = models.ForeignKey(Feature)
	attribute = models.ForeignKey(Attribute)
	value = models.CharField(max_length=255,blank=True,null=True)
