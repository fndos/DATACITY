# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from dash.base import DashboardPluginFormBase
from main import services

__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'

TABLE_TYPE_CHOICES = (
  (None, 'Choose an option'),
  ('variables', 'Variable'),
  ('measurements', 'Measurement'),
  ('station_types', 'StationType'),
  ('stations', 'Station'),
)

API_TYPE_CHOICES = (
  (None, 'Choose an option'),
  ('bubble', 'Station'),
  ('mixed', 'Variable, Station'),
  ('sunburst', 'Mixed Sources'),
)

TREE_MAP_TYPE_CHOICES = (
  (None, 'Choose an option'),
  ('treemap', 'Tree Map: Censo Mundial'),
)

# Formulario para Bar Chart
class BarChartForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
        ("selected_label", ""),
        ("selected_source", ""),
        ("selected_domain", ""),
        ("selected_range", ""),
        ("selected_color", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
    selected_label = forms.CharField(label=_("Etiqueta"), required=True)
    selected_source = forms.ChoiceField(label=_("Tabla/API"), choices=TABLE_TYPE_CHOICES, required=True)
    selected_domain = forms.CharField(label=_("Dominio"), required=True)
    selected_range = forms.CharField(label=_("Rango"), required=True)
    selected_color = forms.CharField(label=_("Color"), required=True, widget=forms.TextInput(attrs={'type':'color'}))

# Formulario para Bubble Chart
class BubbleChartForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
        ("selected_source", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
    selected_source = forms.ChoiceField(label=_("Tabla/API"), choices=API_TYPE_CHOICES, required=True)

# Formulario para Sunburst Partition Chart
class SunburstPartitionChartForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
        ("selected_source", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
    selected_source = forms.ChoiceField(label=_("Tabla/API"), choices=API_TYPE_CHOICES, required=True)

# Formulario para Tree Map
class TreeMapForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
        ("selected_source", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
    selected_source = forms.ChoiceField(label=_("Tabla/API"), choices=TREE_MAP_TYPE_CHOICES, required=True)

# Clase base de la cual heredan todos los charts
class ChartForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
