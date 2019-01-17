# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .formatChecker import validate_file_extension_xml, validate_file_extension_config
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

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)
class Simulation(models.Model):
	# osm.motorcycle.rou.xml
	# osm.passenger.trips.xml
	# osm_bbox.osm.xml
	# osm.motorcycle.trips.xml
	# osm.polycfg
	# osm.bus.rou.alt.xml
	# osm.netccfg
	# osm.poly.xml
	# osm.bus.rou.xml
	# osm.net.xml
	# osm.sumocfg
	# osm.bus.trips.xml
	# osm.passenger.rou.alt.xml
	# osm.view.xml
	# osm.motorcycle.rou.alt.xml
	# osm.passenger.rou.xml
	mapa_red=models.FileField(verbose_name="Mapa de la simulacion", upload_to=user_directory_path, validators=[validate_file_extension_xml])
	# RUTAS y VIAJES POR TIPO DE VEHICULO
	rutas_bus = models.FileField(verbose_name="Mapa de rutas de buses", upload_to=user_directory_path, validators=[validate_file_extension_xml])
	# rutas_alt_bus = models.FileField(verbose_name="Mapa de rutas alternas de buses", upload_to=user_directory_path, validators=[validate_file_extension_xml])
	viajes_bus = models.FileField(verbose_name="Archivo de viajes de buses", upload_to=user_directory_path, validators=[validate_file_extension_xml])
	rutas_moto = models.FileField(verbose_name="Mapa de rutas de motos", upload_to=user_directory_path, validators=[validate_file_extension_xml])
	# rutas_alt_moto = models.FileField(verbose_name="Mapa de rutas alternas de motos", upload_to=user_directory_path, validators=[validate_file_extension_xml])
	viajes_moto = models.FileField(verbose_name="Archivo de viajes de motos", upload_to=user_directory_path, validators=[validate_file_extension_xml])
	rutas_carro = models.FileField(verbose_name="Mapa de rutas de carros", upload_to=user_directory_path, validators=[validate_file_extension_xml])
	# rutas_carro = models.FileField(verbose_name="Mapa de rutas alternas de carros", upload_to=user_directory_path, validators=[validate_file_extension_xml])
	viajes_carro = models.FileField(verbose_name="Archivo de viajes de carros", upload_to=user_directory_path, validators=[validate_file_extension_xml])
	poly_file =	models.FileField(verbose_name="Archivo de configuracion de poligonos", upload_to=user_directory_path, validators=[validate_file_extension_xml])
	view_file = models.FileField(verbose_name="Archivo de configuracion de vista", upload_to=user_directory_path, validators=[validate_file_extension_xml])

	#ARCHIVOS DE CONFIGURACION
	config_red = models.FileField(verbose_name="Archivo netccfg", upload_to=user_directory_path, validators=[validate_file_extension_config])
	config_poly = models.FileField(verbose_name="Archivo netccfg", upload_to=user_directory_path, validators=[validate_file_extension_config])
	config_sumo = models.FileField(verbose_name="Archivo netccfg", upload_to=user_directory_path, validators=[validate_file_extension_config])

	class Meta:
		verbose_name="Simulacion"
		verbose_name_plural="Simulaciones"
