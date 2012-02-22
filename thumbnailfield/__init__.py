#!/usr/bin/env python
# vim: set fileencoding=utf8:
try:
    from PIL import Image
except ImportError:
    import Image
from django.conf import settings

def setconfig(name, default_value):
    value = getattr(settings, name, default_value)
    setattr(settings, name, value)

setconfig('THUMBNAILFIELD_REMOVE_PREVIOUS', True)
setconfig('THUMBNAILFIELD_DEFAULT_PROCESS_METHOD', 'thumbnail')
setconfig('THUMBNAILFIELD_DEFAULT_PROCESS_OPTIONS', {'resample': Image.ANTIALIAS})
setconfig('THUMBNAILFIELD_FILENAME_PATTERN', r"%(root)s/%(filename)s.%(name)s.%(ext)s")

import process_methods
DEFAULT_PROCESS_METHOD_TABLE = {
        'thumbnail': process_methods.get_thumbnail_image,
        'resize': process_methods.get_resized_image,
        'crop': process_methods.get_cropped_image,
        'grayscale': process_methods.get_grayscale_image,
        'sepia': process_methods.get_sepia_image,
    }
setconfig('THUMBNAILFIELD_PROCESS_METHOD_TABLE', DEFAULT_PROCESS_METHOD_TABLE)
