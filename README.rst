``django-thumbnailfield`` is a enhanced ImageField of Django

It has the follwing features

-   Using Django storage system to store the image (Not like other Thumbnail library)
-   Automatically remove previous file from storage
-   Automatically generate thumbnails
-   Automatically remove generated previous thumbnail files from storage
-   Easy to use custom method to generate thumbnails

Install
===========================================
::

	sudo pip install django-thumbnailfield


Prepare to use
==========================================

1.  Append 'thumbnailfield' to ``INSTALLED_APPS``

2.  Set ``MEDIA_ROOT`` correctly. For example::

    MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '../static')


Example mini blog app
=========================================

``models.py``::
	
	from django.db import models
	from django.contrib.auth.models import User

    from thumbnailfield.fields import ThumbnailField
	
	class Entry(models.Model):
		PUB_STATES = (
			('public', 'public entry'),
			('protected', 'login required'),
			('private', 'secret entry'),
		)
		pub_state = models.CharField('publish status', choices=PUB_STATES)
		title = models.CharField('title', max_length=140)
		body = models.TextField('body')

        #
        # This is a usage of ThumbnailField.
        # You have to set ``patterns`` to generate thumbnails
        #
        thumbnail = ThumbnailField(_('thumbnail'), upload_to='img/thumbnails', null=True, blank=True, patterns={
                # Pattern Format:
                #   <Name>: (
                #   (<square_size>,),       # with defautl process_method
                #   (<width>, <height>,),   # with default process_method
                #   (<width>, <height>, <method or method_name>),
                #   (<width>, <height>, <method or method_name>, <method options>),
                #   )
                #
                # If Name is ``None`` that mean original image will be processed
                # with the pattern
                #
                # Convert original image to sepia and resize it to 800x400 (original
                # size is 804x762)
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
                #   # shortcut properties
                #   entry.thumbnail.large_file  # as entry.thumbnail.large.file
                #   entry.thumbnail.large_path  # as entry.thumbnail.large.path
                #   entry.thumbnail.large_url   # as entry.thumbnail.large.url
                #   entry.thumbnail.large.size  # as entry.thumbnail.large.size
                #
            })
		# ...

``entry_detail.html``::

	<html>
	<head>
		<title>django-thumbnailfield example</title>
	</head>
	<body>
	    <dl>
	        <dt>Original</dt>
	        <dd><img src="{{ MEDIA_URL }}{{ object.thumbnail }}"></dd>
	        <dt>Thumbnail "large"</dt>
	        <dd><img src="{{ MEDIA_URL }}{{ object.thumbnail.large }}"></dd>
	        <dt>Thumbnail "small"</dt>
	        <dd><img src="{{ MEDIA_URL }}{{ object.thumbnail.small }}"></dd>
	        <dt>Thumbnail "tiny"</dt>
	        <dd><img src="{{ MEDIA_URL }}{{ object.thumbnail.tiny }}"></dd>
	    </dl>
	</body>
	</html>

How to use custom process method
================================================================

Create your own custom process method like below::

    from thumbnailfield.process_methods import get_sepia_image
    from thumbnailfield.process_methods import get_cropped_image
    from thumbnailfield.exceptions import ThumbnailFieldPatternImproperlyConfigured

    def get_sepia_and_cropped_image(img, width, height, **options):
        # do something with img
        img = get_sepia_image(img, None, None, **options)
        img = get_cropped_image(img, width, height, **options)
        return img
    def _sepia_and_cropped_error_check(f, img, width, height, **options):
        # do some error check
        if 'left' not in options:
            raise ThumbnailFieldPatternImproperlyConfigured(f, "'left' is required")
        if 'upper' not in options:
            raise ThumbnailFieldPatternImproperlyConfigured(f, "'upper' is required")
    # Apply error check function
    # Error check is recommended if your process method required any options
    # otherwise just forget about this.
    get_sepia_and_cropped_image.error_check = _sepia_and_cropped_error_check
        
Use defined method in pattern like below

    # models.py
    # ...
    thumbnail = ThumbnailField('thumbnail', upload_to='thumbnails', patterns = {
            'large': (400, 500, get_sepia_and_cropped_image, {'left': 0, 'upper': 0})
        }
    # ...

Or define the method in THUMBNAILFIELD_PROCESS_METHOD_TABLE and use as a string anme

    # settings.py
    from thumbnailfield import DEFAULT_PROCESS_METHOD_TABLE
    THUMBNAILFIELD_PROCESS_METHOD_TABLE = DEFAULT_PROCESS_METHOD_TABLE
    THUMBNAILFIELD_PROCESS_METHOD_TABLE['sepia_and_crop'] = get_sepia_and_cropped_image

    # models.py
    # ...
    thumbnail = ThumbnailField('thumbnail', upload_to='thumbnails', patterns = {
            'large': (400, 500, 'sepia_and_crop', {'left': 0, 'upper': 0})
        }
    # ...

Settings
=========================================
``THUMBNAILFIELD_REMOVE_PREVIOUS``
    Remove previous files (include original file) when new file is applied to
    the ThumbnailField.

    Default: ``True``

``THUMBNAILFIELD_DEFAULT_PROCESS_METHOD``
    Used when no process_method is applied in process pattern.

    Default: ``thumbnail``

``THUMBNAILFIELD_DEFAULT_PROCESS_OPTIONS``
    Used when no process_options is applied in process pattern.

    Default: ``{'resample': Image.ANTIALIAS}``

``THUMBNAILFIELD_FILENAME_PATTERN``
    Used to determine thumbnail filename. ``root``, ``filename``, ``name``
    and ``ext`` is passed to the string. The generated filename of the 
    thumbnail named 'large' of '/some/where/test.png' will be 
    ``/some/where/test.large.png`` in default.

    Default: ``r"%(root)s/%(filename)s.%(name)s.%(ext)s"``

``THUMBNAILFIELD_PROCESS_METHOD_TABLE``
    Used to determine process method from string name. The key of this dictionary
    is a name of the method and value is a method.

    ``thumbnail``, ``resize``, ``crop``, ``grayscale`` and ``sepia`` are defined
    as default.

    Default: See ``thumbnailfield.__init__.DEFAULT_PROCESS_METHOD_TABLE``
