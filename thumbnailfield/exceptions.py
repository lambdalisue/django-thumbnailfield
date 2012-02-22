#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Exceptions used in django-thumbnailfield


AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = "lambdalisue (lambdalisue@hashnote.net)"

class ThumbnailFieldPatternImproperlyConfigured(Exception):
    """ThumbnailField Process Pattern is not configured properly."""
    def __init__(self, f, msg):
        cls = f.instance.__class__
        module_name = cls.__module__
        class_name = cls.__name__
        attr_name = f.field.attname
        where = r"%s.%s.%s" % (module_name, class_name, attr_name)
        msg = "%s [at %s]" % (msg, where)
        super(ThumbnailFieldPatternImproperlyConfigured, self).__init__(msg)
