# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.conf import settings
from appconf import AppConf

from thumbnailfield import process_methods
from thumbnailfield.compatibility import Image


DEFAULT_PROCESS_METHOD_TABLE = {
    'thumbnail': process_methods.get_thumbnail_image,
    'resize': process_methods.get_resized_image,
    'crop': process_methods.get_cropped_image,
    'grayscale': process_methods.get_grayscale_image,
    'sepia': process_methods.get_sepia_image,
}


class ThumbnailFieldConf(AppConf):
    REMOVE_PREVIOUS = False
    DEFAULT_PROCESS_METHOD = 'thumbnail'
    DEFAULT_PROCESS_OPTIONS = {'resample': Image.ANTIALIAS}
    FILENAME_PATTERN = r'%(root)s/%(filename)s.%(name)s.%(ext)s'
    PROCESS_METHOD_TABLE = DEFAULT_PROCESS_METHOD_TABLE
