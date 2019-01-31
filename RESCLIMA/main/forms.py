# -*- coding: utf-8 -*-
from django import forms
from . models import *

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
			'identity_card': forms.TextInput(),
			'first_name': forms.TextInput(),
			'last_name': forms.TextInput(),
			'username': forms.TextInput(),
			'password': forms.PasswordInput(),
			'email': forms.TextInput(),
			'institution': forms.TextInput(),
			'phone_number': forms.TextInput(),
		}

	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		self.fields['username'].help_text = None

class LogisticaForm(forms.ModelForm):
	class Meta:
		model = Logistica
		fields = ('__all__')
	file = forms.FileField(required=True)

class ClimaForm(forms.ModelForm):
	class Meta:
		model = Clima
		fields = ('__all__')
	file = forms.FileField(required=True)

class CensoForm(forms.ModelForm):
	class Meta:
		model = Censo
		fields = ('__all__')
	file = forms.FileField(required=True)
