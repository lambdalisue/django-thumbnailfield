# vim: set fileencoding=utf8:
from setuptools import setup, find_packages

version = '0.1.0'

def read(filename):
    import os.path
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name="django-thumbnailfield",
    version=version,
    description = "Enhanced ImageField which automatically generate thumbnails of the image",
    long_description=read('README.rst'),
    classifiers = [
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords = "django fields image thumbnail",
    author = "Alisue",
    author_email = "lambdalisue@hashnote.net",
    url=r"https://github.com/lambdalisue/django-thumbnailfield",
    download_url = r"https://github.com/lambdalisue/django-thumbnailfield/tarball/master",
    license = 'MIT',
    packages = find_packages(),
    include_package_data = True,
    install_requires=[
        'distribute',
        'setuptools-git',
        'PIL',
    ],
    test_suite='tests.runtests.runtests',
    tests_require=[
        'django>=1.3',
        'PyYAML',
    ],
)
