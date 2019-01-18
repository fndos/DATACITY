from django.template.loader import render_to_string
from django.conf import settings

from ....base import BaseDashboardPluginWidget

__title__ = 'dash.contrib.plugins.file.dash_widgets'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyrighat__ = '2013-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'BaseFileWidget',
    'File1x1Widget',
    'File1x2Widget',
    'File2x1Widget',
    'File2x2Widget',
    'File2x3Widget',
    'File3x2Widget',
    'File3x3Widget',
    'File3x4Widget',
    'File4x3Widget',
    'File4x4Widget',
    'File4x5Widget',
    'File5x4Widget',
    'File5x5Widget',
)

# **********************************************************************
# ************************ Base File widget plugin ********************
# **********************************************************************


class BaseFileWidget(BaseDashboardPluginWidget):
    """Base file plugin widget."""

    media_js = (
        'js/dash_plugin_file.js',
    )
    media_css = (
        'css/dash_plugin_file.css',
    )

    def render(self, request=None):
        """Render."""
        context = {
            'plugin': self.plugin,
            'MEDIA_URL': settings.MEDIA_URL
        }
        return render_to_string('file/render.html', context)

# **********************************************************************
# ************************** Specific widgets **************************
# **********************************************************************


class File1x1Widget(BaseFileWidget):
    """File1x1 plugin widget."""

    plugin_uid = 'file_1x1'


class File1x2Widget(BaseFileWidget):
    """File1x2 plugin widget."""

    cols = 1
    rows = 2
    plugin_uid = 'file_1x2'


class File2x1Widget(BaseFileWidget):
    """File2x1 plugin widget."""

    cols = 2
    rows = 1
    plugin_uid = 'file_2x1'


class File2x2Widget(BaseFileWidget):
    """File2x2 plugin widget."""

    cols = 2
    rows = 2
    plugin_uid = 'file_2x2'


class File2x3Widget(BaseFileWidget):
    """File2x3 plugin widget."""

    cols = 2
    rows = 3
    plugin_uid = 'file_2x3'


class File3x2Widget(BaseFileWidget):
    """File3x2 plugin widget."""

    cols = 3
    rows = 2
    plugin_uid = 'file_3x2'


class File3x3Widget(BaseFileWidget):
    """File3x3 plugin widget."""

    cols = 3
    rows = 3
    plugin_uid = 'file_3x3'


class File3x4Widget(BaseFileWidget):
    """File3x4 plugin widget."""

    cols = 3
    rows = 4
    plugin_uid = 'file_3x4'


class File4x4Widget(BaseFileWidget):
    """File4x4 plugin widget."""

    cols = 4
    rows = 4
    plugin_uid = 'file_4x4'


class File4x5Widget(BaseFileWidget):
    """File4x5 plugin widget."""

    cols = 4
    rows = 5
    plugin_uid = 'file_4x5'


class File5x4Widget(BaseFileWidget):
    """File5x4 plugin widget."""

    cols = 5
    rows = 4
    plugin_uid = 'file_5x4'


class File5x5Widget(BaseFileWidget):
    """File5x5 plugin widget."""

    cols = 5
    rows = 5
    plugin_uid = 'file_5x5'
