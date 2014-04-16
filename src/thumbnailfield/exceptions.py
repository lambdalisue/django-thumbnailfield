# coding=utf-8
"""
Exceptions used in django-thumbnailfield
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.core.exceptions import ImproperlyConfigured

class ThumbnailFieldPatternImproperlyConfigured(ImproperlyConfigured):
    """ThumbnailField Process Pattern is not configured properly."""
    def __init__(self, f, msg):
        cls = f.instance.__class__
        module_name = cls.__module__
        class_name = cls.__name__
        attr_name = f.field.attname
        where = r"%s.%s.%s" % (module_name, class_name, attr_name)
        msg = "%s [at %s]" % (msg, where)
        super(ThumbnailFieldPatternImproperlyConfigured, self).__init__(msg)
