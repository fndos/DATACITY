import glob
import logging
import os
import shutil
import uuid

from django.conf import settings
from django.core.files.base import File

from .settings import (
    FILES_UPLOAD_DIR,
)

__title__ = 'dash.contrib.plugins.file.helpers'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'clone_file',
    'delete_file',
    'ensure_unique_filename',
    'handle_uploaded_file',
)


logger = logging.getLogger(__file__)

FILES_UPLOAD_DIR_ABSOLUTE_PATH = os.path.join(settings.MEDIA_ROOT,
                                               FILES_UPLOAD_DIR)
if not os.path.exists(FILES_UPLOAD_DIR_ABSOLUTE_PATH):
    os.makedirs(FILES_UPLOAD_DIR_ABSOLUTE_PATH)


def ensure_unique_filename(destination):
    """Ensure unique filename.

    Makes sure filenames are never overwritten. If file name already exists,
    makes a new one based on the first 50 chars of the original file name,
    having a uuid4 appended afterwards.

    :param string destination:
    :return string:
    """
    if os.path.exists(destination):
        dest, filename = os.path.split(destination)
        filename, extension = os.path.splitext(filename)
        return os.path.join(
            dest, "{0}_{1}{2}".format(filename[:30], uuid.uuid4(), extension)
        )
    else:
        return destination


def handle_uploaded_file(file_file):
    """Handle uploaded file.

    :param django.core.files.uploadedfile.InMemoryUploadedFile file_file:
    :return string: Path to the file (relative).
    """
    if isinstance(file_file, File):
        destination_path = ensure_unique_filename(
            os.path.join(FILES_UPLOAD_DIR_ABSOLUTE_PATH, file_file.name)
        )
        file_filename = file_file.name
        with open(destination_path, 'wb+') as destination:
            file_filename = os.path.basename(destination.name)
            for chunk in file_file.chunks():
                destination.write(chunk)
        return os.path.join(FILES_UPLOAD_DIR, file_filename)
    return file_file

def delete_file(file_file):
    """Delete file from disc."""
    try:
        # Delete the main file.
        file_path = os.path.join(settings.MEDIA_ROOT, file_file)
        os.remove(file_path)

        # Delete the sized version of it.
        files = glob.glob("{0}*".format(file_path))
        for _file in files:
            try:
                os.remove(_file)
            except Exception as err:
                logger.debug(str(err))

        # If all goes well...
        return True
    except Exception as err:
        logger.debug(str(err))
        return False


def clone_file(source_filename, relative_path=True):
    """Clone the file.

    :param string source_filename: Source filename.
    :param str relative_path:
    :return string: Filename of the cloned file.
    """
    if source_filename.startswith(FILES_UPLOAD_DIR):
        source_filename = os.path.join(settings.MEDIA_ROOT, source_filename)

    destination_filename = ensure_unique_filename(source_filename)
    try:
        shutil.copyfile(source_filename, destination_filename)
        if relative_path:
            destination_filename = destination_filename.replace(
                settings.MEDIA_ROOT, ''
            )
            if destination_filename.startswith('/'):
                destination_filename = destination_filename[1:]
        return destination_filename
    except Exception as err:
        logger.debug(str(err))
