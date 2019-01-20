from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.validators import FileExtensionValidator

from ....base import DashboardPluginFormBase
from ....widgets import BooleanRadioSelect

from .helpers import handle_uploaded_file


__title__ = 'dash.contrib.plugins.file.forms'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('FileForm',)


class FileForm(forms.Form, DashboardPluginFormBase):
    """Files form for `FilesPlugin` plugin."""

    plugin_data_fields = [
        ("title", ""),
        ("file", "")
    ]

    title = forms.CharField(label=_("Title"), required=True)
    file = forms.FileField(label=_("File"), required=True,  validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    def save_plugin_data(self, request=None):
        """Saving the plugin data and moving the file."""
        file = self.cleaned_data.get('file', None)
        if file:
            saved_file = handle_uploaded_file(file)
            self.cleaned_data['file'] = saved_file
