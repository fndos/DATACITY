# -*- coding: utf-8 -*-
from django import forms
from . models import *

class SimulationForm(forms.ModelForm):
	class Meta:
		model = Simulation
		fields = ['name', 'step', 'sumo_config']
	file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

class LogisticaForm(forms.ModelForm):
	class Meta:
		model = Logistica
		fields = ('__all__')
	file = forms.FileField(required=True)
