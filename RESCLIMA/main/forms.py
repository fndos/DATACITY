# -*- coding: utf-8 -*-
from django import forms
from . models import *
from django.db.models import Q

################################# MANAGER ######################################

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'identity_card',
			'first_name',
			'last_name',
			'username',
			'password',
			'email',
			'institution',
			'phone_number',
			'user_type',
		]
		labels = {
			'identity_card': 'Cédula/Pasaporte',
			'first_name': 'Nombre',
			'last_name': 'Apellido',
			'username': 'Usuario',
			'password': 'Contraseña',
			'email': 'Correo electrónico',
			'institution': 'Institución',
			'phone_number': 'Teléfono',
			'user_type': 'Tipo de usuario',
		}
		widgets = {
			'identity_card': forms.TextInput(attrs={'class':'form-control'}),
			'first_name': forms.TextInput(attrs={'class':'form-control'}),
			'last_name': forms.TextInput(attrs={'class':'form-control'}),
			'username': forms.TextInput(attrs={'class':'form-control'}),
			'password': forms.PasswordInput(attrs={'class':'form-control'}),
			'email': forms.TextInput(attrs={'class':'form-control'}),
			'institution': forms.TextInput(attrs={'class':'form-control'}),
			'phone_number': forms.TextInput(attrs={'class':'form-control'}),
			'user_type': forms.Select(attrs={'class':'form-control'}),
		}

	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		self.fields['username'].help_text = None
