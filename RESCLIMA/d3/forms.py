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
  # Choices con datos de RESCLIMA
  ('db_resclima_average_measurement', 'RESCLIMA: Promedio de mediciones por variable'),
  # Choices con datos de logistica y transporte
  ('d3_bar_chart_L_EN', 'Circulación de vehiculos livianos en GD Sentido E-N'),
  # ('d3_bar_chart_L_EO', 'Circulación de vehiculos livianos en FR Sentido E-O'),
  # ('d3_bar_chart_L_NO', 'Circulación de vehiculos livianos en GD Sentido N-O'),
  # ('d3_bar_chart_L_ON', 'Circulación de vehiculos livianos en GI Sentido O-N'),
  # ('d3_bar_chart_L_OE', 'Circulación de vehiculos livianos en GD Sentido O-E'),
  # ('d3_bar_chart_L_NE', 'Circulación de vehiculos livianos en GD Sentido N-E'),
  ('d3_bar_chart_W_EN', 'Circulación de vehiculos pesados en GD Sentido E-N'),
  # ('d3_bar_chart_W_EO', 'Circulación de vehiculos pesados en FR Sentido E-O'),
  # ('d3_bar_chart_W_NO', 'Circulación de vehiculos pesados en GD Sentido N-O'),
  # ('d3_bar_chart_W_ON', 'Circulación de vehiculos pesados en GI Sentido O-N'),
  # ('d3_bar_chart_W_OE', 'Circulación de vehiculos pesados en GD Sentido O-E'),
  # ('d3_bar_chart_W_NE', 'Circulación de vehiculos pesados en GD Sentido N-E'),
  # Choices solo para SUMO | Emisiones
  ('d3_line_chart_WMS', 'SUMO: Velocidad promedio de vehiculos pesados'),
  ('d3_line_chart_LMS', 'SUMO: Velocidad promedio de vehiculos livianos'),
  ('d3_line_chart_WT', 'SUMO: Tiempo de espera promedio de vehiculos pesados'),
  ('d3_line_chart_LT', 'SUMO: Tiempo de espera promedio de vehiculos livianos'),
  # Datos de Censo
  ('d3_bar_chart_censo', 'Censo (Hombres, Mujeres)'), # No se mira bien
  ('d3_bar_chart_population', 'Censo (Total Poblacion)')  # No se mira bien
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

PIE_CHART_CHOICES = (
  (None, 'Selecciona una opción'),
  # Datos de Censo
  ('d3_pie_chart_censo', 'Censo (Hombres, Mujeres)'),
  ('d3_pie_chart_WE', 'SUMO: Emisiones de gases de vehiculos pesados'),
  ('d3_pie_chart_LE', 'SUMO: Emisiones de gases de vehiculos livianos'),
  # Choices con datos de logistica y transporte
  ('d3_pie_chart_composition_EN', 'Composicion de vehicular E-N giro a la derecha'),
  ('d3_pie_chart_composition_EO', 'Composicion de vehicular E-O frente'),
  ('d3_pie_chart_composition_NO', 'Composicion de vehicular N-O giro a la derecha'),
  ('d3_pie_chart_composition_ON', 'Composicion de vehicular O-N giro a la izquierda'),
  ('d3_pie_chart_composition_OE', 'Composicion de vehicular O-E frente'),
  ('d3_pie_chart_composition_NE', 'Composicion de vehicular N-E giro a la izquierda'),

)
TIME_SERIES_CHOICES = (
  (None, 'Selecciona una opción'),
  ('d3_grouped_bar_chart', 'Precipitacion'), # Mover a Z Time Series
)
TIME_SERIES_CHOICES = (
  (None, 'Selecciona una opción'),
  ('d3_time_series_oni', 'Oceanic Niño Index (ONI)'), # Mover a Z Time Series
  ('d3_time_series_rr', 'Relative Risk (RR)'),
)

# Z_TIME_SERIES_CHOICES = ((None, 'Selecciona una opción'),)

MULTI_TIME_SERIES_CHOICES = (
  (None, 'Selecciona una opción'),
  ('d3_time_series_tmax', 'Temperatura Maxima'),
  ('d3_time_series_tmean', 'Temperatura Media'),
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

class GroupedBarChartForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
        ("start_date", ""),
        ("end_date", ""),
        # ("domainLabel", ""),
        ("rangeLabel", ""),
        # ("simulation", ""),
        ("source", ""),
        # ("color", ""),
        # ("hover", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
    # domainLabel = forms.CharField(label=_("Etiqueta del eje X"), required=True)
    rangeLabel = forms.CharField(label=_("Etiqueta del eje Y"), required=True)
    start_date = forms.CharField(label=_("Fecha de inicio"), required=False, widget=forms.TextInput(attrs={'type':'date'}))
    end_date = forms.CharField(label=_("Fecha de finalizacion"), required=False, widget=forms.TextInput(attrs={'type':'date'}))
    source = forms.ChoiceField(label=_("Tabla/API"), choices=TIME_SERIES_CHOICES, required=True)




# Formulario para Time Series
class TimeSeriesForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
        ("rangeLabel", ""),
        ("start_date", ""),
        ("end_date", ""),
        ("source", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
    rangeLabel = forms.CharField(label=_("Etiqueta del eje Y"), required=True)
    start_date = forms.CharField(label=_("Fecha de inicio"), required=False, widget=forms.TextInput(attrs={'type':'date'}))
    end_date = forms.CharField(label=_("Fecha de finalizacion"), required=False, widget=forms.TextInput(attrs={'type':'date'}))
    source = forms.ChoiceField(label=_("Tabla/API"), choices=TIME_SERIES_CHOICES, required=True)

# Formulario para Multi Time Series
class MultiTimeSeriesForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
        ("rangeLabel", ""),
        ("start_date", ""),
        ("end_date", ""),
        ("source", ""),
        ("origin", ""),
        ("outset", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
    rangeLabel = forms.CharField(label=_("Etiqueta del eje Y"), required=True)
    start_date = forms.CharField(label=_("Fecha de inicio"), required=False, widget=forms.TextInput(attrs={'type':'date'}))
    end_date = forms.CharField(label=_("Fecha de finalizacion"), required=False, widget=forms.TextInput(attrs={'type':'date'}))
    source = forms.ChoiceField(label=_("Tabla/API"), choices=MULTI_TIME_SERIES_CHOICES, required=True)
    origin = forms.ChoiceField(label=_("Tabla/API"), choices=MULTI_TIME_SERIES_CHOICES, required=True)
    outset = forms.ChoiceField(label=_("Tabla/API"), choices=MULTI_TIME_SERIES_CHOICES, required=True)

# Formulario para Pie Chart
class PieChartForm(forms.Form, DashboardPluginFormBase):

    plugin_data_fields = [
        ("title", ""),
        ("simulation", ""),
        ("source", ""),
        ("start_date", ""),
        ("end_date", ""),
    ]

    title = forms.CharField(label=_("Titulo"), required=True)
    start_date = forms.CharField(label=_("Fecha de inicio"), required=False, widget=forms.TextInput(attrs={'type':'date'}))
    end_date = forms.CharField(label=_("Fecha de finalizacion"), required=False, widget=forms.TextInput(attrs={'type':'date'}))

    def __init__(self, *args, **kwargs):
        super(PieChartForm, self).__init__(*args, **kwargs)
        SIMULATION_CHOICES = [(None, 'Selecciona una opción')]
        TEMP = [(s.id, s) for s in  models.Simulation.objects.all()]
        for i in range(len(TEMP)):
            SIMULATION_CHOICES.append(TEMP[i])
        self.fields['simulation'] = forms.ChoiceField(label=_("Simulacion [Solo en caso de que quiera utilizar datos de SUMO]"), choices=SIMULATION_CHOICES, required=False)
        self.fields['source'] = forms.ChoiceField(label=_("Tabla/API"), choices=PIE_CHART_CHOICES, required=True)

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
