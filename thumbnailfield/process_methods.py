#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Builtin ThumbnailField process methods


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
try:
    from PIL import ImageOps
except ImportError:
    import ImageOps
from exceptions import ThumbnailFieldPatternImproperlyConfigured

def get_grayscale_image(img, width, height, **options):
    """get grayscale image"""
    grayscale = img.copy()
    if img.mode != 'L':
        grayscale = grayscale.convert('L')
    return grayscale
def _grayscale_error_check(f, img, width, height, **options):
    # grayscale pattern doesn't require width/height
    if width is not None or height is not None:
        raise ThumbnailFieldPatternImproperlyConfigured(f, "'width' and 'height' must be None in 'grayscale' pattern")
get_grayscale_image.error_check = _grayscale_error_check

def get_sepia_image(img, width, height, **options):
    """get sepia image"""
    def make_linear_ramp(white):
        # putpalette expects [r,g,b,r,g,b,...]
        ramp = []
        r, g, b = white
        for i in range(255):
            ramp.extend((r*i/255, g*i/255, b*i/255))
        return ramp
    sepia = make_linear_ramp((255, 240, 192))

    # make the image grayscale
    grayscale = get_grayscale_image(img, width, height, **options)

    # optional: apply contrast enhancement here, e.g.
    grayscale = ImageOps.autocontrast(grayscale)

    # apply sepia palette
    grayscale.putpalette(sepia)

    # convert back to RGB so we can save it as JPEG
    # (alternatively, save it in PNG or similar)
    return grayscale.convert("RGB")
def _sepia_error_check(f, img, width, height, **options):
    # sepia pattern doesn't require width/height
    if width is not None or height is not None:
        raise ThumbnailFieldPatternImproperlyConfigured(f, "'width' and 'height' must be None in 'sepia' pattern")
get_sepia_image.error_check = _sepia_error_check

def get_cropped_image(img, width, height, left, upper, **options):
    """get cropped image
    
    Attribute:
        img -- PIL image instance
        width -- width of thumbnail
        height -- height of thumbnail
        left -- left point of thumbnail
        upper -- upper point of thumbnail
        kwargs -- Options used in PIL thumbnail method
        
    Usage::
        >>> try:
        ...     from PIL import Image
        ... except ImportError:
        ...     import Image
        >>> img = Image.new('RGBA', (1000, 800))
        >>> thumb = get_cropped_image(img, 100, 100, 0, 0)
        >>> assert thumb.size[0] == 100
        >>> assert thumb.size[1] == 100
    """
    right = left + width
    lower = upper + height
    thumbs = img.crop((left, upper, right, lower))
    return thumbs
def _cropped_error_check(f, img, width, height, **options):
    # crop pattern required left/upper options
    if 'left' not in options:
        raise ThumbnailFieldPatternImproperlyConfigured(f, "'crop' pattern required 'left' option")
    if 'upper' not in options:
        raise ThumbnailFieldPatternImproperlyConfigured(f, "'crop' pattern required 'upper' option")
get_cropped_image.error_check = _cropped_error_check

def get_resized_image(img, width, height, force=False, **options):
    """get resized image
    
    Attribute:
        img -- PIL image instance
        width -- width of thumbnail
        height -- height of thumbnail
        kwargs -- Options used in PIL thumbnail method
        
    Usage::
        >>> try:
        ...     from PIL import Image
        ... except ImportError:
        ...     import Image
        >>> img = Image.new('RGBA', (1000, 800))
        >>> thumb = get_resized_image(img, 100, 100)
        >>> assert thumb.size[0] == 100
        >>> assert thumb.size[1] == 100
    """
    thumbs = img.copy()
    if force or img.size[0] > width or img.size[1] > height:
        thumbs = img.resize(size=(width, height), **options)
    return thumbs

def get_thumbnail_image(img, width, height, **options):
    """get thumbnail image
    
    Attribute:
        img -- PIL image instance
        width -- width of thumbnail
        height -- height of thumbnail
        kwargs -- Options used in PIL thumbnail method
        
    Usage::
        >>> try:
        ...     from PIL import Image
        ... except ImportError:
        ...     import Image
        >>> img = Image.new('RGBA', (1000, 800))
        >>> thumb = get_thumbnail_image(img, 100, 100)
        >>> assert thumb.size[0] == 100
        >>> assert thumb.size[1] == 80
    """
    thumbs = img.copy()
    thumbs.thumbnail(size=(width, height), **options)
    return thumbs
