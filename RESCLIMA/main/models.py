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
	identity_card =models.CharField(max_length=10, unique=False) # Must be unique=True
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

	def __unicode__(self):
		return "%s %s" % (self.first_name, self.last_name)

	def __str__(self):
		return "%s %s" % (self.first_name, self.last_name)

	class Meta:
		verbose_name = "User"
		verbose_name_plural = "Users"
