from django.utils.translation import ugettext_lazy as _

from ....base import BaseDashboardPlugin
from ....factory import plugin_factory

from .forms import FileForm
from .helpers import delete_file, clone_file

__title__ = 'dash.contrib.plugins.file.dash_plugins'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('BaseFilePlugin',)


# ****************************************************************************
# ***************************** Base File plugin ****************************
# ****************************************************************************


class BaseFilePlugin(BaseDashboardPlugin):
    """Base file plugin."""

    name = _("File")
    group = _("File")
    form = FileForm
    html_classes = ['pictonic']

    def delete_plugin_data(self):
        """Deletes uploaded file."""
        delete_file(self.data.file)

    def clone_plugin_data(self, dashboard_entry):
        """Clone plugin data, which means we make a copy of the original file.

        TODO: Perhaps rely more on data of ``dashboard_entry``?
        """
        cloned_file = clone_file(self.data.file, relative_path=True)
        return self.get_cloned_plugin_data(update={'file': cloned_file})


# ****************************************************************************
# ********** Generating and registering the plugins using factory ************
# ****************************************************************************


sizes = (
    (1, 1),
    (1, 2),
    (2, 1),
    (2, 2),
    (2, 3),
    (3, 2),
    (3, 3),
    (3, 4),
    (4, 3),
    (4, 4),
    (4, 5),
    (5, 4),
    (5, 5)
)

plugin_factory(BaseFilePlugin, 'file', sizes)
