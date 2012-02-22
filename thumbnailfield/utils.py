#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Utilities of ThumbnailField


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
import os
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from django.conf import settings
from django.core.files.base import ContentFile

def get_content_file(img, file_fmt, **kwargs):
    """get ContentFile from PIL image instance with file_fmt

    Attributes:
        img -- PIL Image instance
        file_fmt -- Saved image format (PNG, JPEG, ...)
        kwargs -- Options used in PIL image save method

    Usage::
        >>> try:
        ...     from PIL import Image
        ... except ImportError:
        ...     import Image
        >>> from django.core.files.base import ContentFile
        >>> img = Image.new('RGBA', (100, 100))
        >>> cf = get_content_file(img, 'PNG')
        >>> assert isinstance(cf, ContentFile)
    """
    
    file_obj = StringIO()
    img.save(file_obj, format=file_fmt, **kwargs)
    return ContentFile(file_obj.getvalue())

def save_to_storage(img, storage, filename, overwrite=False, **kwargs):
    """save PIL image instance to Django storage with filename

    Attributes:
        img -- PIL Image instance
        storage -- Django storage instance
        filename -- filename
        overwrite -- If true, delete existing file first
        kwargs -- Options used in PIL image save method

    Usage::
        >>> try:
        ...     from PIL import Image
        ... except ImportError:
        ...     import Image
        >>> from django.core.files.storage import FileSystemStorage
        >>> img = Image.new('RGBA', (100, 100))
        >>> storage = FileSystemStorage()
        >>> filename = 'test.png'
        >>> # save image to storage
        >>> filename_ = save_to_storage(img, storage, filename)
        >>> # file exists
        >>> assert storage.exists(filename_)
        >>> # resave
        >>> filename_ = save_to_storage(img, storage, filename)
        >>> # used different filename
        >>> assert filename != filename_
        >>> storage.delete(filename_)
        >>> # overwrite the file
        >>> filename_ = save_to_storage(img, storage, filename, overwrite=True)
        >>> assert filename == filename_
        >>> storage.delete(filename)
    """
    file_fmt = get_fileformat_from_filename(filename)
    content_file = get_content_file(img, file_fmt, **kwargs)
    if overwrite and storage.exists(filename):
        storage.delete(filename)
    return storage.save(filename, content_file)

def get_thumbnail_filename(path, name, pattern=None):
    """get thumbnail filename with name and pattern
    
    Attributes:
        path -- original path
        name -- thumbnail name
        pattern -- file name generation pattern (default = settings.THUMBNAILFIELD_FILENAME_PATTERN)

    Usage::
        >>> path = "/some/where/test.png"
        >>> name = "small"
        >>> pattern = r"%(root)s/%(filename)s.%(name)s.%(ext)s"
        >>> thumb_filename = get_thumbnail_filename(path, name, pattern)
        >>> assert thumb_filename == "/some/where/test.small.png"
    """
    pattern = pattern or settings.THUMBNAILFIELD_FILENAME_PATTERN
    root, filename = path.rsplit('/', 1)
    filename, ext = os.path.splitext(filename)
    path = pattern % {
            'root': root,
            'filename': filename,
            'name': name,
            'ext': ext[1:],
        }
    return path

def get_fileformat_from_filename(filename):
    """get fileformat from filename
    
    Attributes:
        filename -- filename used to guess fileformat

    Usage::
        >>> assert get_fileformat_from_filename("test.png") == "PNG"
        >>> assert get_fileformat_from_filename("test.jpg") == "JPEG"
        >>> assert get_fileformat_from_filename("test.jpe") == "JPEG"
        >>> assert get_fileformat_from_filename("test.jpeg") == "JPEG"
        >>> assert get_fileformat_from_filename("test.gif") == "GIF"
        >>> assert get_fileformat_from_filename("test.tif") == "TIFF"
        >>> assert get_fileformat_from_filename("test.tiff") == "TIFF"
        >>> assert get_fileformat_from_filename("test.bmp") == "BMP"
        >>> assert get_fileformat_from_filename("test.dib") == "BMP"
        >>> assert get_fileformat_from_filename("/some/where/test.png") == "PNG"
    """
    patterns = (
            (['.png'], 'PNG'),
            (['.jpg', '.jpe', '.jpeg'], 'JPEG'),
            (['.gif'], 'GIF'),
            (['.tif', '.tiff'], 'TIFF'),
            (['.bmp', '.dib'], 'BMP'),
            (['.dcx'], 'DCX'),
            (['.eps', 'ps'], 'EPS'),
            (['.im'], 'IM'),
            (['.pcd'], 'PCD'),
            (['.pcx'], 'PCX'),
            (['.pdf'], 'PDF'),
            (['.pbm', '.pgm', '.ppm'], 'PPM'),
            (['.psd'], 'PSD'),
            (['.xbm'], 'XBM'),
            (['.xpm'], 'XPM')
        )
    if '.' not in filename:
        return None
    ext = os.path.splitext(filename)[1]
    for pattern in patterns:
        if ext in pattern[0]:
            return pattern[1]
    return None

def _split_pattern(pattern):
    process_method = None
    process_options = settings.THUMBNAILFIELD_DEFAULT_PROCESS_OPTIONS
    if len(pattern) == 1:
        width = height = pattern[0]
    if len(pattern) == 2:
        width, height = pattern
    elif len(pattern) == 3:
        width, height, process_method = pattern
    elif len(pattern) == 4:
        width, height, process_method, process_options = pattern
    process_method = process_method or settings.THUMBNAILFIELD_DEFAULT_PROCESS_METHOD
    return width, height, process_method, process_options

def get_processed_image(f, img, patterns):
    """process PIL image with pattern attribute
    
    Attributes:
        f -- ThumbnailFieldFile instance
        img -- PIL Image instance
        patterns -- Process patterns

    pattern format is shown below::

        # Use default process_method with default process options and same width, height
        pattern = [square_size]
        # Use default process_method with default process options and width, height
        pattern = [width, height]
        # Use process_method with default process options and width, height
        pattern = [width, height, process_method]
        # Use process_method with process_options with widht, height
        pattern = [width, height, process_method, process_options]

    default process_method and process_options are configured in settings.py as::

        THUMBNAILFIELD_DEFAULT_PROCESS_METHOD = 'thumbnail'
        THUMBNAILFIELD_DEFAULT_PROCESS_OPTIONS = {'filter': Image.ANTIALIAS}
    """
    processed = img.copy()
    if not isinstance(patterns[0], (list, tuple)):
        patterns = [patterns]
    for pattern in patterns:
        width, height, process_method, process_options = _split_pattern(pattern)
        process_method_table = settings.THUMBNAILFIELD_PROCESS_METHOD_TABLE
        for method_name, method in process_method_table.iteritems():
            if process_method == method_name:
                if getattr(method, 'error_check', None):
                    method.error_check(f, img, width, height, **process_options)
                process_method = method
                break
        if not callable(process_method):
            raise AttributeError('process_method have to be a string name defined in THUMBNAILFIELD_PROCESS_METHOD_TABLE or method.')
        processed = process_method(processed, width, height, **process_options)
    return processed
