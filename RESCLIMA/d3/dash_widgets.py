from django.template.loader import render_to_string
from django.conf import settings

from dash.base import BaseDashboardPluginWidget

__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2014-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'

# *************************************************************
# ***************** Base chart widget *************************
# *************************************************************


class BaseChartWidget(BaseDashboardPluginWidget):
    """Base chart widget."""

    _template = None

    def render(self, request=None):
        """Render."""
        context = {
            'plugin': self.plugin,
            'width': self.get_width(),
            'height': self.get_height(),
            'STATIC_URL': settings.STATIC_URL,
        }
        return render_to_string(
            self._template,
            context
        )


class BaseBubbleChartWidget(BaseChartWidget):
    """Base bubble chart widget."""

    media_js = (
        'js/d3.v3.min.js',  # Main D3 script
        'js/d3_bubble_chart.js',  # Helper script
    )
    _template = 'd3_samples/plugins/render_d3_bubble_chart.html'


class BaseStackedToGroupedBarsChartWidget(BaseChartWidget):
    """Stacked-to-grouped bars chart widget."""

    media_js = (
        'js/d3.v3.min.js',  # Main D3 script
        'js/d3_stacked_to_grouped_bars_chart.js',  # Helper script
    )

    media_css = (
        'css/d3_stacked_to_grouped_bars_chart.css',  # Specific styles
    )

    _template = 'd3_samples/plugins/render_stacked_to_grouped_bars_chart.html'


class BaseSunburstPartitionChartWidget(BaseChartWidget):
    """Sunburst partition chart widget."""

    media_js = (
        'js/d3.v3.min.js',  # Main D3 script
        'js/d3_sunburst_partition_chart.js',  # Helper script
    )

    media_css = (
        'css/d3_sunburst_partition_chart.css',  # Specific styles
    )

    _template = 'd3_samples/plugins/render_d3_sunburst_partition_chart.html'

class BaseBarChartWidget(BaseChartWidget):
    """Bar partition chart widget."""

    media_js = (
        'js/d3.v3.min.js',  # Main D3 script
        'js/d3.tip.min.js', # D3 Tip Script
        'js/d3_bar_chart.js',  # Helper script
    )

    media_css = (
        'css/d3_bar_chart.css',  # Specific styles
    )

    _template = 'd3_samples/plugins/render_d3_bar_chart.html'

class BaseTreeMapWidget(BaseChartWidget):
    """Bar partition chart widget."""

    media_js = (
        'js/d3.v3.min.js',  # Main D3 script
        'js/d3_tree_map.js',  # Helper script
    )

    media_css = (
        'css/d3_tree_map.css',  # Specific styles
    )

    _template = 'd3_samples/plugins/render_d3_tree_map.html'

class BaseTimeSeriesWidget(BaseChartWidget):
    """Bar partition chart widget."""

    media_js = (
        'js/d3.v3.min.js',  # Main D3 script
        'js/d3_time_series.js',  # Helper script
    )

    media_css = (
        'css/d3_time_series.css',  # Specific styles
    )

    _template = 'd3_samples/plugins/render_d3_time_series.html'
