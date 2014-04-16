# coding=utf-8
"""
Compatibility module
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'

# PIL image
try:
   from PIL import Image 
   from PIL import ImageOps
except ImportError:
    import Image
    import ImageOps

# StringIO
try:
    from io import BytesIO as StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

