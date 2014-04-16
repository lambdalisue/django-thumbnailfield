# run doctests and unittests; for django under 1.6
import doctest
import unittest

list_of_doctests = (
    'thumbnailfield.process_methods',
    'thumbnailfield.utils',
    'thumbnailfield.fields',
)
list_of_unittests = (
    'thumbnailfield.tests.test_thubmanilfield',
)

def suite():
    suite = unittest.TestSuite()
    for t in list_of_doctests:
        suite.addTest(doctest.DocTestSuite(
            __import__(t, globals(), locals(), fromlist=["*"])
        ))
    for t in list_of_unittests:
        suite.addTest(unittest.TestLoader().loadTestsFromModule(
            __import__(t, globals(), locals(), fromlist=["*"])
        ))
    return suite
