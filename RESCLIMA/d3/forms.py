# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from dash.base import DashboardPluginFormBase
from main import services

__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'

TABLE_TYPE_CHOICES = (
  (None, 'Selecciona una opción'),
  ('lon', 'Vehiculos | Liviano | GD O-N'),
  ('loe', 'Vehiculos | Liviano | FR O-E'),
  ('lne', 'Vehiculos | Liviano | GD N-E'),
  ('won', 'Vehiculos | Pesado | GD O-N'),
  ('woe', 'Vehiculos | Pesado | FR O-E'),
  ('wne', 'Vehiculos | Pesado | GD O-N'),
)

PIE_TYPE_CHOICES = (
  (None, 'Selecciona una opción'),
  ('d3_pie_chart_composition_ON', 'Composicion Vehicular | GD O-N'),
  ('d3_pie_chart_composition_OE', 'Composicion Vehicular | FR O-E'),
  ('d3_pie_chart_composition_NE', 'Composicion Vehicular | GD N-E'),
  ('d3_pie_chart_composition', 'Composicion Vehicular | TODAS'),
)

API_TYPE_CHOICES = (
  (None, 'Selecciona una opción'),
  ('bubble', 'Station'),
  ('mixed', 'Variable, Station'),
  ('sample', 'Bubble Sample (name, size)'),
  ('sunburst', 'Mixed Sources'),
)

TREE_MAP_TYPE_CHOICES = (
  (None, 'Selecciona una opción'),
  ('treemap', 'Tree Map: Censo Mundial'),
)

# Formulario para Bar Chart
class BarChartForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
        ("date", ""),
        ("domainLabel", ""),
        ("rangeLabel", ""),
        ("source", ""),
        ("color", ""),
        ("hover", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
    domainLabel = forms.CharField(label=_("Etiqueta del eje X"), required=True)
    rangeLabel = forms.CharField(label=_("Etiqueta del eje Y"), required=True)
    date = forms.CharField(label=_("Fecha"), required=True, widget=forms.TextInput(attrs={'type':'date'}))
    source = forms.ChoiceField(label=_("Tabla/API"), choices=TABLE_TYPE_CHOICES, required=True)
    color = forms.CharField(label=_("Color principal"), required=True, widget=forms.TextInput(attrs={'type':'color'}))
    hover = forms.CharField(label=_("Color secundario"), required=True, widget=forms.TextInput(attrs={'type':'color'}))

# Formulario para Bubble Chart
class BubbleChartForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
        ("source", ""),
        ("key", ""),
        ("value", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
    source = forms.ChoiceField(label=_("Tabla/API"), choices=API_TYPE_CHOICES, required=True)
    key = forms.CharField(label=_("Key"), required=False, strip=True)
    value = forms.CharField(label=_("Value"), required=False, strip=True)

# Formulario para Sunburst Partition Chart
class SunburstPartitionChartForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
        ("source", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
    source = forms.ChoiceField(label=_("Tabla/API"), choices=API_TYPE_CHOICES, required=True)

# Formulario para Tree Map
class TreeMapForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
        ("source", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
    source = forms.ChoiceField(label=_("Tabla/API"), choices=TREE_MAP_TYPE_CHOICES, required=True)

# Formulario para Tree Map
class TimeSeriesForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)

# Formulario para Pie Chart
class PieChartForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
        ("source", ""),
        ("date", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
    source = forms.ChoiceField(label=_("Tabla/API"), choices=PIE_TYPE_CHOICES, required=True)
    date = forms.CharField(label=_("Fecha"), required=True, widget=forms.TextInput(attrs={'type':'date'}))

class LineChartForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
        ("source", ""),
        ("date", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
    source = forms.ChoiceField(label=_("Tabla/API"), choices=TABLE_TYPE_CHOICES, required=True)
    date = forms.CharField(label=_("Fecha"), required=True, widget=forms.TextInput(attrs={'type':'date'}))

# Clase base de la cual heredan todos los charts
class ChartForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
