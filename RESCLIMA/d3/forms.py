# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from dash.base import DashboardPluginFormBase
from main import services
from simulation import models

__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'

KEY_VALUE_CHOICES = (
  (None, 'Selecciona una opción'),
  ('db_resclima_average_measurement', 'Promedio | Variable | Estacion'),
  ('d3_bar_chart_L_ON', 'Vehiculos | Liviano | GD O-N'),
  ('d3_bar_chart_L_OE', 'Vehiculos | Liviano | FR O-E'),
  ('d3_bar_chart_L_NE', 'Vehiculos | Liviano | GD N-E'),
  ('d3_bar_chart_W_ON', 'Vehiculos | Pesado | GD O-N'),
  ('d3_bar_chart_W_OE', 'Vehiculos | Pesado | FR O-E'),
  ('d3_bar_chart_W_NE', 'Vehiculos | Pesado | GD N-E'),
  # Choices solo para SUMO | Emisiones
  ('d3_line_chart_KV_W_CO2', 'SUMO | Emisiones de CO2 | Pesado'),
  ('d3_line_chart_KV_L_CO2', 'SUMO | Emisiones de CO2 | Liviano'),
  ('d3_line_chart_KV_W_CO', 'SUMO | Emisiones de CO | Pesado'),
  ('d3_line_chart_KV_L_CO', 'SUMO | Emisiones de CO | Liviano'),
)

  # ('d3_bar_chart_L_EN', 'GD Sentido E-N | Liviano'), # noexiste
  # ('d3_bar_chart_L_EO', 'FR Sentido E-O | Liviano'), # noexiste
  # ('d3_bar_chart_L_NO', 'GD Sentido N-O | Liviano'), # noexiste
  # ('d3_bar_chart_L_ON', 'GI Sentido O-N | Liviano'),
  # ('d3_bar_chart_L_OE', 'GD Sentido O-E | Liviano'),
  # ('d3_bar_chart_L_NE', 'GD Sentido N-E | Liviano'),
  # ('d3_bar_chart_W_EN', 'GD Sentido E-N | Pesado'), # noexiste
  # ('d3_bar_chart_W_EO', 'FR Sentido E-O | Pesado'), # noexiste
  # ('d3_bar_chart_W_NO', 'GD Sentido N-O | Pesado'), # noexiste
  # ('d3_bar_chart_W_ON', 'GI Sentido O-N | Pesado'),
  # ('d3_bar_chart_W_OE', 'GD Sentido O-E | Pesado'),
  # ('d3_bar_chart_W_NE', 'GD Sentido N-E | Pesado'),

MOVEMENT_TYPE_CHOICES = (
  (None, 'Seleccione una opción'),
  (1, 'GD Sentido E-N'),
  (2, 'FR Sentido E-O'),
  (3, 'GD Sentido N-O'),
  (4, 'GI Sentido O-N'),
  (5, 'FR Sentido O-E'),
  (6, 'GI Sentido N-E'),
)

PIE_CHART_CHOICES = (
  (None, 'Selecciona una opción'),
  ('d3_pie_chart_composition_ON', 'Composicion Vehicular | GD O-N'),
  ('d3_pie_chart_composition_OE', 'Composicion Vehicular | FR O-E'),
  ('d3_pie_chart_composition_NE', 'Composicion Vehicular | GD N-E'),
  ('d3_pie_chart_composition', 'Composicion Vehicular | TODAS'),
)

BUBBLE_CHART_CHOICES = (
  (None, 'Selecciona una opción'),
  ('d3_bubble_chart_AVG_WE', 'Emisiones | W'),
  ('d3_bubble_chart_AVG_LE', 'Emisiones | L'),
)

TREE_MAP_CHOICES = (
  (None, 'Selecciona una opción'),
  ('d3_tree_map_sample', 'Tree Map: Censo Mundial'),
)

TIME_SERIES_CHOICES = (
  (None, 'Selecciona una opción'),
  ('d3_time_series_tmin', 'Temperatura Minima'),
)

# Formulario para Bar Chart
class BarChartForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
        ("start_date", ""),
        ("end_date", ""),
        ("domainLabel", ""),
        ("rangeLabel", ""),
        ("simulation", ""),
        ("source", ""),
        ("color", ""),
        ("hover", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
    domainLabel = forms.CharField(label=_("Etiqueta del eje X"), required=True)
    rangeLabel = forms.CharField(label=_("Etiqueta del eje Y"), required=True)
    start_date = forms.CharField(label=_("Fecha de inicio"), required=False, widget=forms.TextInput(attrs={'type':'date'}))
    end_date = forms.CharField(label=_("Fecha de finalizacion"), required=False, widget=forms.TextInput(attrs={'type':'date'}))

    def __init__(self, *args, **kwargs):
        super(BarChartForm, self).__init__(*args, **kwargs)
        SIMULATION_CHOICES = [(None, 'Selecciona una opción')]
        TEMP = [(s.id, s) for s in  models.Simulation.objects.all()]
        for i in range(len(TEMP)):
            SIMULATION_CHOICES.append(TEMP[i])
        self.fields['simulation'] = forms.ChoiceField(label=_("Simulacion [Solo en caso de que quiera utilizar datos de SUMO]"), choices=SIMULATION_CHOICES, required=False)
        self.fields['source'] = forms.ChoiceField(label=_("Tabla/API"), choices=KEY_VALUE_CHOICES, required=True)
        self.fields['color'] = forms.CharField(label=_("Color principal"), required=True, widget=forms.TextInput(attrs={'type':'color'}))
        self.fields['hover'] = forms.CharField(label=_("Color secundario"), required=True, widget=forms.TextInput(attrs={'type':'color'}))

# Formulario para Bubble Chart
class BubbleChartForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
        ("simulation", ""),
        ("source", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)

    def __init__(self, *args, **kwargs):
        super(BubbleChartForm, self).__init__(*args, **kwargs)
        SIMULATION_CHOICES = [(None, 'Selecciona una opción')]
        TEMP = [(s.id, s) for s in  models.Simulation.objects.all()]
        for i in range(len(TEMP)):
            SIMULATION_CHOICES.append(TEMP[i])
        self.fields['simulation'] = forms.ChoiceField(label=_("Simulacion [Solo en caso de que quiera utilizar datos de SUMO]"), choices=SIMULATION_CHOICES, required=False)
        self.fields['source'] = forms.ChoiceField(label=_("Tabla/API"), choices=BUBBLE_CHART_CHOICES, required=True)


# Formulario para Tree Map
class TreeMapForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
        ("source", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
    source = forms.ChoiceField(label=_("Tabla/API"), choices=TREE_MAP_CHOICES, required=True)

# Formulario para Time Series
class TimeSeriesForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
        ("source", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
    source = forms.ChoiceField(label=_("Tabla/API"), choices=TIME_SERIES_CHOICES, required=True)

# Formulario para Pie Chart
class PieChartForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
        ("source", ""),
        ("date", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
    source = forms.ChoiceField(label=_("Tabla/API"), choices=PIE_CHART_CHOICES, required=True)
    date = forms.CharField(label=_("Fecha"), required=False, widget=forms.TextInput(attrs={'type':'date'}))

# Formulario para Line Chart
class LineChartForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
        ("domainLabel", ""),
        ("rangeLabel", ""),
        ("start_date", ""),
        ("end_date", ""),
        ("simulation", ""),
        ("source", ""),
        ("origin", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
    domainLabel = forms.CharField(label=_("Etiqueta del eje X"), required=True)
    rangeLabel = forms.CharField(label=_("Etiqueta del eje Y"), required=True)
    start_date = forms.CharField(label=_("Fecha de inicio"), required=False, widget=forms.TextInput(attrs={'type':'date'}))
    end_date = forms.CharField(label=_("Fecha de finalizacion"), required=False, widget=forms.TextInput(attrs={'type':'date'}))

    def __init__(self, *args, **kwargs):
        super(LineChartForm, self).__init__(*args, **kwargs)
        SIMULATION_CHOICES = [(None, 'Selecciona una opción')]
        TEMP = [(s.id, s) for s in  models.Simulation.objects.all()]
        for i in range(len(TEMP)):
            SIMULATION_CHOICES.append(TEMP[i])
        self.fields['simulation'] = forms.ChoiceField(label=_("Simulacion [Solo en caso de que quiera utilizar datos de SUMO]"), choices=SIMULATION_CHOICES, required=False)
        self.fields['source'] = forms.ChoiceField(label=_("Tabla/API"), choices=KEY_VALUE_CHOICES, required=True)
        self.fields['origin'] = forms.ChoiceField(label=_("Tabla/API"), choices=KEY_VALUE_CHOICES, required=True)

# Clase base de la cual heredan todos los charts
class ChartForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
