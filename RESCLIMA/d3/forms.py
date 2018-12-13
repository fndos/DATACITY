# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from dash.base import DashboardPluginFormBase
from d3.models import Graph
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'


class ChartForm(forms.Form, DashboardPluginFormBase):
    """Chart form for `ChartBasePlugin` plugin."""

    plugin_data_fields = [
        ("title", ""),
    ]

    title = forms.CharField(label=_("Title"), required=True)






#FIX
    # class ChartForm(forms.ModelForm, DashboardPluginFormBase):
    # """Chart form for `ChartBasePlugin` plugin."""
    # class Meta:
    # 	model = Graph
    # 	fields = ['name','clients', 'graph_label']
    # #title = forms.CharField(label=_("Title"), required=True)
    # plugin_data_fields = [
    #     ("name", "clients", "graph_label"),
    # ]

