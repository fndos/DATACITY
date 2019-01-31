# -*- coding: utf-8 -*-
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.core.validators import FileExtensionValidator

class User(AbstractUser):
	# Type Choices: User, Customer, Manager
	USER_TYPE_CHOICES = (
	  (None, 'Seleccione una opción'),
	  (1, 'Administrador'),
	  (2, 'Investigador'),
	  (3, 'Cliente'),
	)
	# Información General
	identity_card = models.CharField(max_length=10, unique=False) # Must be unique=True
	phone_number = models.CharField(max_length=10)
	institution = models.CharField(max_length=100)
	user_type = models.PositiveSmallIntegerField(null=True, choices=USER_TYPE_CHOICES)
	# Registro de Actividad
	created_by = models.CharField(max_length=100)
	updated_by = models.CharField(null=True, max_length=100)
	date_updated = models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		self.password = make_password(self.password)
		self.is_superuser = True
		super(User, self).save(*args, **kwargs)

	def get_user_type(self):
		if self.user_type == 1:
			return "Administrador"
		elif self.user_type == 2:
			return "Investigador"
		elif self.user_type == 3:
			return "Cliente"

	def get_user_type(self):
		choices = {
	        1: "Administrador",
	        2: "Investigador",
	        3: "Cliente"
	    }
		return choices.get(self.user_type, "¡Choices error!")

	def __unicode__(self):
		return "%s %s" % (self.first_name, self.last_name)

	def __str__(self):
		return "%s %s" % (self.first_name, self.last_name)

	class Meta:
		verbose_name = "User"
		verbose_name_plural = "Users"

# Modelos para los datos de Logistica y Transporte
class Logistica(models.Model):
	VEHICLE_TYPE_CHOICES = (
	  (None, 'Seleccione una opción'),
	  (1, 'Liviano'),
	  (0, 'Pesado'),
	)
	MOVEMENT_TYPE_CHOICES = (
	  (None, 'Seleccione una opción'),
	  (1, 'GD Sentido E-N'),
	  (2, 'FR Sentido E-O'),
	  (3, 'GD Sentido N-O'),
	  (4, 'GI Sentido O-N'),
	  (5, 'FR Sentido O-E'),
	  (6, 'GI Sentido N-E'),
	)
	# Informacion general
	id_term = models.IntegerField()
	value = models.IntegerField()
	vehicle_type = models.PositiveSmallIntegerField(null=True, choices=VEHICLE_TYPE_CHOICES)
	movement = models.PositiveSmallIntegerField(null=True, choices=MOVEMENT_TYPE_CHOICES)
	id_gauging = models.IntegerField()
	date = models.DateField()
	# Foreign Key
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def get_vehicle_type(self):
		choices = {
	        1: "Liviano",
	        0: "Pesado"
	    }
		return choices.get(self.vehicle_type, "¡Choices error!")

	def get_movement(self):
		choices = {
	        1: "GD Sentido E-N",
	        2: "FR Sentido E-O",
	        3: "GD Sentido N-O",
	        4: "GI Sentido O-N",
	        5: "FR Sentido O-E",
	        6: "GI Sentido N-E"
	    }
		return choices.get(self.movement, "¡Choices error!")

	class Meta:
		verbose_name = "Logistica"
		verbose_name_plural = "Datos de Logistica"

# Modelos para los datos de cambio climatico e islas de calor
class Clima(models.Model):
	# Informacion general
	date = models.DateField()
	tmin = models.DecimalField(decimal_places=2, max_digits=10)
	tmax = models.DecimalField(decimal_places=2, max_digits=10)
	rr = models.DecimalField(decimal_places=2, max_digits=10)
	oni = models.DecimalField(decimal_places=2, max_digits=10)
	# Foreign Key
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Clima"
		verbose_name_plural = "Datos de Clima"

class Censo(models.Model):
	# Informacion general
	year = models.CharField(max_length=4)
	man = models.IntegerField()
	woman = models.IntegerField()
	total_pob = models.IntegerField()
	lettered = models.IntegerField()
	unlettered = models.IntegerField()
	housing = models.IntegerField()
	# Foreign Key
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Censo"
		verbose_name_plural = "Datos de Censo"
