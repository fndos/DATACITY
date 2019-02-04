from django.utils.translation import ugettext_lazy as _

from dash.base import BaseDashboardPlugin
from dash.factory import plugin_factory, plugin_widget_factory


from .dash_widgets import (
    BaseBarChartWidget,
    BaseTimeSeriesWidget,
    BaseMultiTimeSeriesWidget,
    BasePieChartWidget,
    BaseLineChartWidget,
    BaseGroupedBarChartWidget,
)

from .forms import *

__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2014-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'

# *****************************************************************************
# *************************** Base chart plugin *******************************
# *****************************************************************************


class BaseChartPlugin(BaseDashboardPlugin):
    """Base chart plugin."""

    group = _("Grafico estadistico")
    form = ChartForm
    html_classes = ['chartonic']

class BaseBarChartPlugin(BaseChartPlugin):
    """Base bar chart plugin."""

    name = _("Grafico de barras")
    form = BarChartForm
    html_classes = ['chartonic', 'd3-bar-chart-plugin']


class BaseTimeSeriesPlugin(BaseChartPlugin):
    """Base time series plugin."""

    name = _("Series de tiempo")
    form = TimeSeriesForm
    html_classes = ['chartonic', 'd3-time-series-plugin']

class BaseMultiTimeSeriesPlugin(BaseChartPlugin):
    """Base multi time series plugin."""

    name = _("Series de tiempo multiples")
    form = MultiTimeSeriesForm
    html_classes = ['chartonic', 'd3-multi-time-series-plugin']

class BasePieChartPlugin(BaseChartPlugin):
    """Base pie chart plugin."""

    name = _("Grafico circular")
    form = PieChartForm
    html_classes = ['chartonic', 'd3-pie-chart-plugin']

class BaseLineChartPlugin(BaseChartPlugin):
    """Base line chart plugin."""

    name = _("Grafico de lineas")
    form = LineChartForm
    html_classes = ['chartonic', 'd3-line-chart-plugin']

class BaseGroupedBarChartPlugin(BaseChartPlugin):
    """Base line chart plugin."""

    name = _("Grafico de barras agrupadas")
    form = GroupedBarChartForm
    html_classes = ['chartonic', 'd3-grouped-bar-chart-plugin']

# *****************************************************************************
# ********** Generating and registering the plugins using factory *************
# *****************************************************************************


sizes = (
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
)

plugin_factory(BaseBarChartPlugin, 'd3_bar_chart', sizes)
plugin_factory(BaseTimeSeriesPlugin, 'd3_time_series', sizes)
plugin_factory(BaseMultiTimeSeriesPlugin, 'd3_multi_time_series', sizes)
plugin_factory(BasePieChartPlugin, 'd3_pie_chart', sizes)
plugin_factory(BaseLineChartPlugin, 'd3_line_chart', sizes)
plugin_factory(BaseGroupedBarChartPlugin, 'd3_grouped_bar_chart', sizes)

# *****************************************************************************
# ********************************* Registering widgets ***********************
# *****************************************************************************

# Registering chart plugin widgets

plugin_widget_factory(BaseBarChartWidget, 'bootstrap_materialize', 'main', 'd3_bar_chart', sizes)
plugin_widget_factory(BaseTimeSeriesWidget, 'bootstrap_materialize', 'main', 'd3_time_series', sizes)
plugin_widget_factory(BaseMultiTimeSeriesWidget, 'bootstrap_materialize', 'main', 'd3_multi_time_series', sizes)
plugin_widget_factory(BasePieChartWidget, 'bootstrap_materialize', 'main', 'd3_pie_chart', sizes)
plugin_widget_factory(BaseLineChartWidget, 'bootstrap_materialize', 'main', 'd3_line_chart', sizes)
plugin_widget_factory(BaseGroupedBarChartWidget, 'bootstrap_materialize', 'main', 'd3_grouped_bar_chart', sizes)
