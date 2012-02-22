# vim: set fileencoding=utf8:
"""
Mini blog models

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
__VERSION__ = "0.1.0"
from django.db import models
from django.utils.text import ugettext_lazy as _

from thumbnailfield.fields import ThumbnailField

class Entry(models.Model):
    """mini blog entry model
    
    >>> entry = Entry()

    # Attribute test
    >>> assert hasattr(entry, 'title')
    >>> assert hasattr(entry, 'body')
    >>> assert hasattr(entry, 'created_at')
    >>> assert hasattr(entry, 'updated_at')

    # Function test
    >>> assert callable(getattr(entry, '__unicode__'))
    >>> assert callable(getattr(entry, 'get_absolute_url'))
    """
    title = models.SlugField(_('title'), unique=True)
    body = models.TextField(_('body'))

    #
    # This is a usage of ThumbnailField.
    # You have to set ``patterns`` to generate thumbnails
    #
    thumbnail = ThumbnailField(_('thumbnail'), upload_to='img/thumbnails', null=True, blank=True, patterns={
            # Pattern Format:
            #   <Name>: (
            #   (<square_size>,),       # with defautl process_method
            #   (<width>, <height>,),   # with default process_method
            #   (<width>, <height>, <method or method_name>),
            #   (<width>, <height>, <method or method_name>, <method options>),
            #   )
            #
            # If Name is ``None`` that mean original image will be processed
            # with the pattern
            #
            # Convert original image to sepia and resize it to 800x400 (original
            # size is 804x762)
            None: ((None, None, 'sepia'), (800, 400, 'resize')),
            # Create 640x480 resized thumbnail as large.
            'large': ((640, 480, 'resize'),),
            # Create 320x240 cropped thumbnail as small. You can write short
            # pattern if the number of appling pattern is 1
            'small': (320, 240, 'crop', {'left': 0, 'upper': 0}),
            # Create 160x120 thumbnail as tiny (use default process_method to
            # generate)
            'tiny': (160, 120),
            #
            # These thumbnails are not generated while accessed. These can be
            # accessed with the follwoing code::
            #
            #   entry.thumbnail.large
            #   entry.thumbnail.small
            #   entry.thumbnail.tiny
            #
            #   # shortcut properties
            #   entry.thumbnail.large_file  # as entry.thumbnail.large.file
            #   entry.thumbnail.large_path  # as entry.thumbnail.large.path
            #   entry.thumbnail.large_url   # as entry.thumbnail.large.url
            #   entry.thumbnail.large.size  # as entry.thumbnail.large.size
            #
        })

    created_at = models.DateTimeField(_('date and time created'),
            auto_now_add=True)
    updated_at = models.DateTimeField(_('date and time updated'),
            auto_now=True)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('blogs-entry-detail', (), {'slug': self.title})

    def clean(self):
        """custom validation"""
        from django.core.exceptions import ValidationError
        if self.title in ('create', 'update', 'delete'):
            raise ValidationError(
                    """The title cannot be 'create', 'update' or 'delete'""")
