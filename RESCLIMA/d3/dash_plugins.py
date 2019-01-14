from django.utils.translation import ugettext_lazy as _

from dash.base import BaseDashboardPlugin
from dash.factory import plugin_factory, plugin_widget_factory


from .dash_widgets import (
    BaseBubbleChartWidget,
    BaseBarChartWidget,
    BaseTreeMapWidget,
    BaseTimeSeriesWidget,
    BasePieChartWidget,
    BaseLineChartWidget,
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

    group = _("D3 plugins")
    form = ChartForm
    html_classes = ['chartonic']

class BaseBubbleChartPlugin(BaseChartPlugin):
    """Base bubble chart plugin."""

    name = _("Bubble Chart")
    form = BubbleChartForm
    html_classes = ['chartonic', 'd3-bubble-chart-plugin']

class BaseBarChartPlugin(BaseChartPlugin):
    """Base sunburst partition chart plugin."""

    name = _("Bar Chart")
    form = BarChartForm
    html_classes = ['chartonic', 'd3-bar-chart-plugin']

class BaseTreeMapPlugin(BaseChartPlugin):
    """Base sunburst partition chart plugin."""

    name = _("Tree Map")
    form = TreeMapForm
    html_classes = ['chartonic', 'd3-tree-map-plugin']

class BaseTimeSeriesPlugin(BaseChartPlugin):
    """Base sunburst partition chart plugin."""

    name = _("Time Series")
    form = TimeSeriesForm
    html_classes = ['chartonic', 'd3-time-series-plugin']

class BasePieChartPlugin(BaseChartPlugin):
    """Base sunburst partition chart plugin."""

    name = _("Pie Chart")
    form = PieChartForm
    html_classes = ['chartonic', 'd3-pie-chart-plugin']

class BaseLineChartPlugin(BaseChartPlugin):
    """Base sunburst partition chart plugin."""

    name = _("Line Chart")
    form = LineChartForm
    html_classes = ['chartonic', 'd3-line-chart-plugin']


# *****************************************************************************
# ********** Generating and registering the plugins using factory *************
# *****************************************************************************


sizes = (
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
)

plugin_factory(BaseBubbleChartPlugin,
               'd3_bubble_chart',
               sizes)
plugin_factory(BaseBarChartPlugin,
               'd3_bar_chart',
               sizes)
plugin_factory(BaseTreeMapPlugin,
               'd3_tree_map',
               sizes)
plugin_factory(BaseTimeSeriesPlugin,
               'd3_time_series',
               sizes)
plugin_factory(BasePieChartPlugin,
               'd3_pie_chart',
               sizes)
plugin_factory(BaseLineChartPlugin,
               'd3_line_chart',
               sizes)

# *****************************************************************************
# ********************************* Registering widgets ***********************
# *****************************************************************************

# Registering chart plugin widgets

# Bubble Chart
plugin_widget_factory(BaseBubbleChartWidget,
                      'bootstrap_materialize',
                      'main',
                      'd3_bubble_chart',
                      sizes)

# Bar Chart
plugin_widget_factory(BaseBarChartWidget,
                      'bootstrap_materialize',
                      'main',
                      'd3_bar_chart',
                      sizes)

# Tree Map
plugin_widget_factory(BaseTreeMapWidget,
                      'bootstrap_materialize',
                      'main',
                      'd3_tree_map',
                      sizes)

# Time Series
plugin_widget_factory(BaseTimeSeriesWidget,
                      'bootstrap_materialize',
                      'main',
                      'd3_time_series',
                      sizes)

# Pie Chart
plugin_widget_factory(BasePieChartWidget,
                      'bootstrap_materialize',
                      'main',
                      'd3_pie_chart',
                      sizes)

# Line Chart
plugin_widget_factory(BaseLineChartWidget,
                      'bootstrap_materialize',
                      'main',
                      'd3_line_chart',
                      sizes)
