# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'

# above django 1.6 
# ref: https://docs.djangoproject.com/en/dev/releases/1.6/#new-test-runner
# ref: https://docs.python.org/2/library/doctest.html#unittest-api
import unittest
import doctest
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite('thumbnailfield.process_methods'))
    tests.addTests(doctest.DocTestSuite('thumbnailfield.utils'))
    tests.addTests(doctest.DocTestSuite('thumbnailfield.fields'))
    return tests
