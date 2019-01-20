"""
- ``FILES_UPLOAD_DIR`` (string)
"""
from .conf import get_setting

__title__ = 'dash.contrib.plugins.image.settings'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'FILES_UPLOAD_DIR',
)

FILES_UPLOAD_DIR = get_setting('FILES_UPLOAD_DIR')
