# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Gauging(models.Model):
	# Información General
	date = models.DateField(blank=True)
	weather = models.CharField(max_length=100)
	station = models.CharField(max_length=100)
	ts = models.TimeField(blank=True)
	te = models.TimeField(blank=True)

	def __unicode__(self):
		return "%s | %s" % (self.date, self.station)
	def __str__(self):
		return "%s | %s" % (self.date, self.station)

	class Meta:
		verbose_name = "Aforo"
		verbose_name_plural = "Aforos"

class Term(models.Model):
	# Información General
	number = models.IntegerField()
	gauging = models.ForeignKey(Gauging, null=True, on_delete=models.CASCADE)
	ts = models.TimeField(blank=True)
	te = models.TimeField(blank=True)

	def __unicode__(self):
		return "%s | Periodo %s" % (self.gauging, self.number)
	def __str__(self):
		return "%s | Periodo %s" % (self.gauging, self.number)

	class Meta:
		verbose_name = "Periodo"
		verbose_name_plural = "Periodos"

class Vehicle(models.Model):
	# Type Choices: Liviano, Pesado
	VEHICLE_TYPE_CHOICES = (
	  (None, 'Seleccione una opción'),
	  (1, 'Liviano'),
	  (2, 'Pesado'),
	)
	MOVEMENT_TYPE_CHOICES = (
	  (None, 'Seleccione una opción'),
	  (1, 'GD Sentido O-N'),
	  (2, 'FR Sentido O-E'),
	  (3, 'GR Sentido N-E'),
	)
	# Información General
	term = models.ForeignKey(Term, on_delete=models.CASCADE)
	movement = models.PositiveSmallIntegerField(null=True, choices=MOVEMENT_TYPE_CHOICES)
	type = models.PositiveSmallIntegerField(null=True, choices=VEHICLE_TYPE_CHOICES)
	number = models.IntegerField()

	def __unicode__(self):
		return "%s %s %s %s" % (self.term, self.type, self.movement, self.number)

	def __str__(self):
		if self.type == 1:
			type = "Liviano"
		elif self.type == 2:
			type = "Pesado"

		if self.movement == 1:
			movement = "GD Sentido O-N"
		elif self.movement == 2:
			movement = "FR Sentido O-E"
		elif self.movement == 3:
			movement = "GR Sentido N-E"

		return "%s | %s | %s | %s" % (self.term, type, movement, self.number)

	class Meta:
		verbose_name = "Vehiculo"
		verbose_name_plural = "Vehiculos"
