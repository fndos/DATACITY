# -*- coding: utf-8 -*-
from django import forms
from . models import *
from natsort import natsorted

class SimulationForm(forms.ModelForm):
    class Meta:
        model = Simulation
        fields = ['name', 'step', 'net', 'bus_rou', 'bus_rou_alt', 'bus_trips', 'motorcycle_rou', 'motorcycle_rou_alt', 'motorcycle_trips', 'passenger_rou', 'passenger_rou_alt', 'passenger_trips', 'poly_file', 'view_file', 'net_config', 'poly_config', 'sumo_config']
