# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . validators import validate_file_extension_xml, validate_file_extension_config
from django.db import models
from main.models import *
from django.contrib.postgres.fields import JSONField

from . helpers import (
	user_directory_path,
	file_directory_path,
	output_directory_path
)

class Simulation(models.Model):
	# Total 16, en uso 15 archivos de configuracion
	# Informacion general
	name = models.CharField(verbose_name="Nombre", max_length=100)
	step = models.PositiveIntegerField(verbose_name="Step")
	# Archivos de configuracion
	sumo_config = models.FileField(verbose_name="Archivo sumocfg", upload_to=user_directory_path, validators=[validate_file_extension_config])
	# Foreign Key
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	# Campos de auditoria
	date_updated = models.DateTimeField(auto_now=True) # Fecha de modificación

	def save(self, *args, **kwargs):
		if self.id is None:
			saved_sumo_config = self.sumo_config
			self.sumo_config = None
			super(Simulation, self).save(*args, **kwargs)
			self.sumo_config = saved_sumo_config
		super(Simulation, self).save(*args, **kwargs)

	def __unicode__(self):
		return "%s %s" % (self.id, self.name)
	def __str__(self):
		return "%s %s" % (self.id, self.name)

	class Meta:
		verbose_name="Simulacion"
		verbose_name_plural="Simulaciones"

class SimulationFile(models.Model):
	# Informacion general
	file = models.FileField(upload_to=file_directory_path)
	simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)

	def __unicode__(self):
		return "%s" % (self.file)
	def __str__(self):
		return "%s" % (self.file)

	class Meta:
		verbose_name="Archivo"
		verbose_name_plural="Archivos"

class Output(models.Model):
	# Informacion general
	simulation = models.OneToOneField(Simulation, on_delete=models.CASCADE, primary_key=True)
	summary = JSONField()
	avg_trace = JSONField()
	avg_trace_liviano = JSONField()
	avg_emission = JSONField()
	avg_weight_emission = JSONField()
	avg_light_emission = JSONField()
	key_value_weight_mean_speed = JSONField()
	key_value_light_mean_speed = JSONField()
	key_value_weight_waiting = JSONField()
	key_value_light_waiting = JSONField()

	def __unicode__(self):
		return "%s %s %s" % ("Output: ", self.simulation.id, self.simulation.name)
	def __str__(self):
		return "%s %s %s" % ("Output: ", self.simulation.id, self.simulation.name)

	class Meta:
		verbose_name="Resultado"
		verbose_name_plural="Resultados"
