#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Unittest module of ...


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

class EntryViewTestCase(TestCase):
    fixtures = ['test.yaml']

    def test_list_get(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_detail_get(self):
        response = self.client.get('/foo/')
        self.assertEqual(response.status_code, 200)

    def test_detail_get_invalid(self):
        response = self.client.get('/unknown/')
        self.assertEqual(response.status_code, 404)

    def test_create_get(self):
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        response = self.client.post('/create/', {
                'title': 'foobar', 'body': 'foobar'
            })
        self.assertEqual(response.status_code, 302)
        assert Entry.objects.filter(title='foobar').exists()

    def test_create_post_invalid(self):
        response = self.client.post('/create/', {
                'title': '', 'body': ''
            })
        self.assertEqual(response.status_code, 200)
        assert 'This field is required' in response.content

    def test_update_get(self):
        response = self.client.get('/update/2/')
        self.assertEqual(response.status_code, 200)

    def test_update_get_invalid(self):
        response = self.client.get('/update/999/')
        self.assertEqual(response.status_code, 404)

    def test_update_post(self):
        response = self.client.post('/update/2/', {
                'title': 'foobar', 'body': 'foobar'
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Entry.objects.get(pk=2).title, 'foobar')
        self.assertEqual(Entry.objects.get(pk=2).body, 'foobar')

    def test_update_post_invalid(self):
        response = self.client.post('/update/2/', {
                'title': '', 'body': ''
            })
        self.assertEqual(response.status_code, 200)
        assert 'This field is required' in response.content
        self.client.logout()

    def test_delete_get(self):
        response = self.client.get('/delete/2/')
        self.assertEqual(response.status_code, 200)

    def test_delete_get_invalid(self):
        response = self.client.get('/delete/999/')
        self.assertEqual(response.status_code, 404)

    def test_delete_post(self):
        response = self.client.post('/delete/2/')
        self.assertEqual(response.status_code, 302)
        assert not Entry.objects.filter(pk=2).exists()
