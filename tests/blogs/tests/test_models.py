#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Unittest module of models


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
from django.test import TestCase

from ..models import Entry

class EntryModelTestCase(TestCase):
    def test_creation(self):
        """blog.Entry: creation works correctly"""
        entry = Entry(title='foo', body='bar')
        entry.full_clean()
        self.assertEqual(entry.title, 'foo')
        self.assertEqual(entry.body, 'bar')

        entry.save()
        entry = Entry.objects.get(pk=entry.pk)
        self.assertEqual(entry.title, 'foo')
        self.assertEqual(entry.body, 'bar')

    def test_modification(self):
        """blog.Entry: modification works correctly"""
        entry = Entry(title='foo', body='bar')
        entry.full_clean()
        entry.save()

        entry.title = 'foofoo'
        entry.body = 'barbar'
        entry.full_clean()
        entry.save()
        entry = Entry.objects.get(pk=entry.pk)
        self.assertEqual(entry.title, 'foofoo')
        self.assertEqual(entry.body, 'barbar')

    def test_validation(self):
        """blog.Entry: validation works correctly"""
        from django.core.exceptions import ValidationError
        entry = Entry(title='foo', body='bar')
        entry.full_clean()
        entry.save()

        entry.title = ''
        self.assertRaises(ValidationError, entry.full_clean)

        entry.body = ''
        self.assertRaises(ValidationError, entry.full_clean)

        entry.title = '*' * 100
        self.assertRaises(ValidationError, entry.full_clean)

        entry.title = '!#$%&()'
        self.assertRaises(ValidationError, entry.full_clean)

    def test_deletion(self):
        """blog.Entry: deletion works correctly"""
        entry = Entry(title='foo', body='bar')
        entry.full_clean()
        entry.save()

        num = Entry.objects.all().count()
        entry.delete()
        self.assertEqual(Entry.objects.all().count(), num - 1)

    def test_thumbnailfield_creation(self):
        import os.path
        from django.core.files.base import File

        STATIC = os.path.join(os.path.dirname(__file__), '../../static/')
        SRC = os.path.join(STATIC, 'tests/000.jpg')

        f = File(open(SRC, 'rb'), 'test.jpg')
        entry = Entry.objects.create(title='foo', body='bar', thumbnail=f)

        def thumbnail_test(name, width, height):
            path = os.path.realpath(entry.thumbnail._get_thumbnail_filename(name)) 
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
        import os.path
        from django.core.files.base import File

        STATIC = os.path.join(os.path.dirname(__file__), '../../static/')
        SRC = os.path.join(STATIC, 'tests/000.jpg')
        SRC2 = os.path.join(STATIC, 'tests/001.jpg')

        f = File(open(SRC, 'rb'), 'test.jpg')
        entry = Entry.objects.create(title='foo', body='bar', thumbnail=f)
        entry.thumbnail.update_thumbnail_files()

        entry.thumbnail = File(open(SRC2, 'rb'), 'test2.jpg')
        entry.save()

        def thumbnail_test(name, width, height):
            path = os.path.realpath(entry.thumbnail._get_thumbnail_filename(name)) 
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
