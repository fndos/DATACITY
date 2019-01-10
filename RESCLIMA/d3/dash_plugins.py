from django.utils.translation import ugettext_lazy as _

from dash.base import BaseDashboardPlugin
from dash.factory import plugin_factory, plugin_widget_factory


from .dash_widgets import (
    BaseBubbleChartWidget,
    BaseSunburstPartitionChartWidget,
    #BaseStackedToGroupedBarsChartWidget,
    BaseBarChartWidget,
    BaseTreeMapWidget,
    BaseTimeSeriesWidget,
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

# No se esta usando esta clase por el momento
class BaseStackedToGroupedBarsChartPlugin(BaseChartPlugin):
    """Base stacked-to-grouped bars chart plugin."""

    name = _("Stacked-to-grouped bars chart")
    html_classes = ['chartonic', 'd3-stacked-to-grouped-bars-chart-plugin']


class BaseSunburstPartitionChartPlugin(BaseChartPlugin):
    """Base sunburst partition chart plugin."""

    name = _("Sunburst Partition Chart")
    form = SunburstPartitionChartForm
    html_classes = ['chartonic', 'd3-sunburst-partition-chart-plugin']

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
# plugin_factory(BaseStackedToGroupedBarsChartPlugin,
#                'd3_stacked_to_grouped_bars_chart',
#                sizes)
plugin_factory(BaseSunburstPartitionChartPlugin,
               'd3_sunburst_partition_chart',
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

# Stacked-to-grouped bars chart
# plugin_widget_factory(BaseStackedToGroupedBarsChartWidget,
#                       'bootstrap_materialize',
#                       'main',
#                       'd3_stacked_to_grouped_bars_chart',
#                       sizes)

# Sunburst Partition
plugin_widget_factory(BaseSunburstPartitionChartWidget,
                      'bootstrap_materialize',
                      'main',
                      'd3_sunburst_partition_chart',
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
