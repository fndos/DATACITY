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

class BarChartForm(forms.Form, DashboardPluginFormBase):
    """Chart form for `ChartBasePlugin` plugin."""

    plugin_data_fields = [
        ("title", ""),
        ("selected_label", ""),
        ("selected_table", ""),
        ("selected_domain", ""),
        ("selected_range", ""),
        ("selected_color", ""),
    ]

    title = forms.CharField(label=_("Title"), required=True)
    selected_label = forms.CharField(label=_("Label"), required=True)
    selected_table = forms.ChoiceField(label=_("Table"), choices=TABLE_TYPE_CHOICES, required=True)
    selected_domain = forms.CharField(label=_("Domain"), required=True)
    selected_range = forms.CharField(label=_("Range"), required=True)
    selected_color = forms.CharField(label=_("Color"), required=True, widget=forms.TextInput(attrs={'type':'color'}))

class ChartForm(forms.Form, DashboardPluginFormBase):
    """Chart form for `ChartBasePlugin` plugin."""

    plugin_data_fields = [
        ("title", ""),
    ]

    title = forms.CharField(label=_("Title"), required=True)
