# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os
from django.test import TestCase
from django.core.files.base import File
from thumbnailfield.tests.models import Entry
from thumbnailfield.compatibility import override_settings


FILENAME = os.path.join(os.path.dirname(__file__), 'data', 'lambdalisue.bmp')


@override_settings(
    THUMBNAILFIELD_REMOVE_PREVIOUS=True,
)
class ThumbnailFieldTestCase(TestCase):
    def test_thumbnailfield_creation(self):

        f = File(open(FILENAME, 'rb'), 'test.bmp')
        entry = Entry.objects.create(title='foo', body='bar', thumbnail=f)

        def thumbnail_test(name, width, height):
            path = os.path.realpath(
                entry.thumbnail._get_thumbnail_filename(name))
            # the file does not exists while it has not accessed yet
            self.assert_(not os.path.exists(path))
            thumbnail = getattr(entry.thumbnail, name)
            self.assertEqual(thumbnail.path, path)
            # the file exists while it has accessed
            self.assert_(os.path.exists(path))
            self.assert_(thumbnail.width <= width)
            self.assert_(thumbnail.height <= height)

        thumbnail_test('large', 640, 480)
        thumbnail_test('small', 320, 240)
        thumbnail_test('tiny', 160, 120)

        entry.thumbnail.delete()

    def test_thumbnailfield_modification(self):

        f = File(open(FILENAME, 'rb'), 'test.bmp')
        entry = Entry.objects.create(title='foo', body='bar', thumbnail=f)
        entry.thumbnail.update_thumbnail_files()

        entry.thumbnail = File(open(FILENAME, 'rb'), 'test2.bmp')
        entry.save()

        def thumbnail_test(name, width, height):
            path = os.path.realpath(
                entry.thumbnail._get_thumbnail_filename(name))
            # the file does not exists while it has not accessed yet
            self.assert_(not os.path.exists(path))
            thumbnail = getattr(entry.thumbnail, name)
            self.assertEqual(thumbnail.path, path)
            # the file exists while it has accessed
            self.assert_(os.path.exists(path))
            self.assert_(thumbnail.width <= width)
            self.assert_(thumbnail.height <= height)

        thumbnail_test('large', 640, 480)
        thumbnail_test('small', 320, 240)
        thumbnail_test('tiny', 160, 120)

        entry.thumbnail.delete()
