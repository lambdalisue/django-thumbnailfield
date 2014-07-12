# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.db import models
from thumbnailfield.fields import ThumbnailField


class Entry(models.Model):
    title = models.SlugField('title', unique=True)
    body = models.TextField('body')

    #
    # This is a usage of ThumbnailField.
    # You have to set ``patterns`` to generate thumbnails
    #
    thumbnail = ThumbnailField(
        'thumbnail', upload_to='img/thumbnails', null=True, blank=True,
        patterns={
            # Pattern Format:
            #   <Name>: (
            # (<square_size>,),       # with defautl process_method
            # (<width>, <height>,),   # with default process_method
            #   (<width>, <height>, <method or method_name>),
            #   (<width>, <height>, <method or method_name>, <method options>),
            #   )
            #
            # If Name is ``None`` that mean original image will be processed
            # with the pattern
            #
            # Convert original image to sepia and resize it to 800x400 (
            # original size is 804x762)
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
            # shortcut properties
            # entry.thumbnail.large_file  # as entry.thumbnail.large.file
            # entry.thumbnail.large_path  # as entry.thumbnail.large.path
            # entry.thumbnail.large_url   # as entry.thumbnail.large.url
            # entry.thumbnail.large.size  # as entry.thumbnail.large.size
            #
        })

    class Meta:
        app_label = 'thumbnailfield'
