#!/usr/bin/env python
# vim: set fileencoding=utf8:
"""
Model fields of ThumbnailField


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
    from PIL import Image
except ImportError:
    import Image

from django.conf import settings
from django.db.models.fields.files import ImageField
from django.db.models.fields.files import ImageFieldFile
from django.db.models.fields.files import ImageFileDescriptor
from django.utils.text import ugettext_lazy as _

from utils import save_to_storage
from utils import get_content_file
from utils import get_thumbnail_filename
from utils import get_fileformat_from_filename
from utils import get_processed_image
    
class ThumbnailFileDescriptor(ImageFileDescriptor):
    """Enhanced ImageFileDescriptor
    
    Just like the ImageFileDescriptor, but for ThumbnailField. The only difference is
    removing previous Image and Thumbnails from storage when the value has changed.
    """
    def __set__(self, instance, value):
        if settings.THUMBNAILFIELD_REMOVE_PREVIOUS:
            previous_file = instance.__dict__.get(self.field.attname, None)
            if previous_file and isinstance(previous_file, ThumbnailFieldFile):
                previous_files = [previous_file.path]
                for thumbnail_filename in previous_file.iter_thumbnail_filenames():
                    previous_files.append(thumbnail_filename)
            super(ThumbnailFileDescriptor, self).__set__(instance, value)
            if previous_file and isinstance(previous_file, ThumbnailFieldFile):
                current_file = getattr(instance, self.field.attname)
                if previous_file != current_file:
                    for f in previous_files:
                        self.field.storage.delete(f)
        else:
            super(ThumbnailFileDescriptor, self).__set__(instance, value)

class ThumbnailFieldFile(ImageFieldFile):
    """Enhanced ImageFieldFile

    This FieldFile contains thumbnail ImageFieldFile instances
    and these thumbnails are automatically generate when accessed

    Attributes:
        _get_thumbnail_filename -- get thumbnail filename
        _get_image -- get PIL image instance
        _get_thumbnail -- get PIL image instance of thumbnail
        _get_thumbnail_file -- get ImageFieldFile instance of thumbnail
        _create_thumbnail -- create PIL image instance of thumbnail
        _create_thumbnail_file -- create ImageFieldFile instance of thumbnail
        _update_thumbnail_file -- update thumbnail file and return ImageFieldFile instance
        _remove_thumbnail_file -- remove thumbanil file from storage
        iter_pattern_name -- return iterator of pattern name
        get_pattern_name -- return list of pattern name
        iter_thumbnail_filenames -- return iterator of thumbnail filename
        get_thumbnail_filenames -- return list of thumbnail filename
        iter_thumbnail_files -- return iterator of thumbnail file
        get_thumbnail_files -- return list of thumbnail file
        update_thumbnail_files -- update thumbnail files in storage
        remove_thumbnail_files -- remove thumbnail files from storage

    """

    def __init__(self, *args, **kwargs):
        """Constructor"""
        super(ThumbnailFieldFile, self).__init__(*args, **kwargs)
        self.patterns = self.field.patterns

        # create access properties
        for name in self.patterns.iterkeys():
            if name is None:
                # None is for original file thus continue
                continue
            fget = lambda self, name = name: self._get_thumbnail_file(name)
            setattr(ThumbnailFieldFile, name, property(fget=fget))
            fget = lambda self, name = name: self._get_thumbnail_file(name).file
            setattr(ThumbnailFieldFile, '%s_file' % name, property(fget=fget))
            fget = lambda self, name = name: self._get_thumbnail_file(name).path
            setattr(ThumbnailFieldFile, '%s_path' % name, property(fget=fget))
            fget = lambda self, name = name: self._get_thumbnail_file(name).url
            setattr(ThumbnailFieldFile, '%s_url' % name, property(fget=fget))
            fget = lambda self, name = name: self._get_thumbnail_file(name).size
            setattr(ThumbnailFieldFile, '%s_size' % name, property(fget=fget))

    def _get_thumbnail_filename(self, name):
        """get thumbnail filename with name
        
        thumbnail filename is generated with utils.get_thumbnail_filename method.
        original path is path of this field file
        """
        return get_thumbnail_filename(self.path, name)

    def _get_image(self, force=False):
        """get PIL image of this field file
        
        PIL Image instance is cached in '_image_cache' attribute of this instance

        Attribute:
            force -- used to force reload the PIL image instance from storage
        """
        attr_name = '_image_cache'
        if force or not getattr(self, attr_name, None):
            self.seek(0)
            setattr(self, attr_name, Image.open(self.file))
        return getattr(self, attr_name)

    def _get_thumbnail(self, name, force=False):
        """get PIL thumbnail of this field file
        
        PIL Image instance of thumbnail is cached in '_image_<name>_cache' attribute
        of this instance. The instance is created by '_create_thumbnail' method with
        given named patterns

        Attribute:
            name -- A name of thumbnail patterns
            force -- used to force recreate the PIL Image instace from storage
        """
        attr_name = '_image_%s_cache' % name
        if force or not getattr(self, attr_name, None):
            patterns = self.patterns[name]
            setattr(self, attr_name, self._create_thumbnail(patterns))
        return getattr(self, attr_name)

    def _get_thumbnail_file(self, name, force=False):
        """get ImageFieldFile of thumbnail
        
        ImageFieldFile instance is cached in '_thumbnail_file_<name>_cache' attribute
        of this instance. The instance is created by '_create_thumbnail_file' method with
        given named patterns

        Attribute:
            name -- A name of thumbnail patterns
            force -- used to force recreate the ImageFieldFile instance from PIL instance
        """
        attr_name = '_thumbnail_file_%s_cache' % name
        if force or not getattr(self, attr_name, None):
            thumbs_file = self._create_thumbnail_file(name, force)
            setattr(self, attr_name, thumbs_file)
        return getattr(self, attr_name)

    def _create_thumbnail(self, patterns):
        """create PIL thumbnail of this field file
        
        Attribute:
            patterns -- A process patterns to generate thumbnail
        """
        img = self._get_image()
        thumb = get_processed_image(self, img, patterns)
        return thumb

    def _create_thumbnail_file(self, name, force=False):
        """create thumbnail file and return ImageFieldFile
        
        Attribute:
            name -- A name of thumbnail patterns
            force -- used to force recreate PIL image instance from original image
        """
        thumbs = self._get_thumbnail(name, force)
        thumbs_filename = self._get_thumbnail_filename(name)
        save_to_storage(thumbs, self.storage, thumbs_filename, overwrite=True)
        thumbs_file = ImageFieldFile(self.instance, self.field, thumbs_filename)
        return thumbs_file

    def _update_thumbnail_file(self, name):
        """update thumbnail file of storage
        
        Attribute:
            name -- A name of thumbnail patterns
        """
        return self._get_thumbnail_file(name, force=True)

    def _remove_thumbnail_file(self, name, save=True):
        """remove thumbnail file from storage
        
        Attribute:
            name -- A name of thumbnail patterns
            save -- If true, the model instance of this field will be saved
        """
        attr_name = '_thumbnail_file_%s_cache' % name
        thumbs_file = getattr(self, attr_name, None)
        if thumbs_file:
            thumbs_file.delete(save)
            delattr(self, attr_name)
    
    def iter_pattern_names(self):
        """return iterator of thumbnail pattern names"""
        return self.patterns.iterkeys()

    def get_pattern_names(self):
        """return list of thumbnail pattern names"""
        pattern_names = [n for n in self.iter_pattern_names()]
        return pattern_names

    def iter_thumbnail_filenames(self):
        """return iterator of thumbnail filenames"""
        for name in self.iter_pattern_names():
            yield self._get_thumbnail_filename(name)

    def get_thumbnail_filenames(self):
        """return list of thumbnail filenames"""
        thumbnail_filenames = [f for f in self.iter_thumbnail_filenames()]
        return thumbnail_filenames

    def iter_thumbnail_files(self):
        """return iterator of thumbnail files"""
        for name in self.iter_pattern_names():
            yield self._get_thumbnail_file(name)

    def get_thumbnail_files(self):
        """return list of thumbnail files"""
        thumbnail_files = [f for f in self.iter_thumbnail_files()]
        return thumbnail_files
            
    def update_thumbnail_files(self):
        """update thumbanil files of storage"""
        for name in self.iter_pattern_names():
            self._update_thumbnail_file(name)
    
    def remove_thumbnail_files(self, save=True):
        """remove thumbnail files from storage
        
        Attribute:
            save -- If true, the model instance of this field will be saved.
        """
        for name in self.iter_pattern_names():
            self._remove_thumbnail_file(name, save=False)
        if save:
            self.instance.save()

    def save(self, name, content, save=True):
        if self and not self._committed and None in self.patterns:
            # Apply original image process
            img = self._get_image()
            processed = get_processed_image(self, img, self.patterns[None])
            file_fmt = get_fileformat_from_filename(name)
            content = get_content_file(processed, file_fmt)
        super(ThumbnailFieldFile, self).save(name, content, save=save)

    def delete(self, save=True):
        self.remove_thumbnail_files(save=False)
        super(ThumbnailFieldFile, self).delete(save=save)

class ThumbnailField(ImageField):
    """Enhanced ImageField

    ThumbnailField has the follwoing features

    -   Automatically remove previous file
    -   Automatically generate thumbnail files
    -   Automatically remove generated previous thumbnail files
    """
    attr_class = ThumbnailFieldFile
    descriptor_class = ThumbnailFileDescriptor
    description = _("Thumbnail")

    def __init__(self, verbose_name=None, name=None, width_field=None, 
            height_field=None, patterns=None, **kwargs):
        """Constructor

        Patterns:
            patterns attribute is used to generate thumbnail files (or apply
            processes to original file). The format of this attribute is::

                patterns = {
                    <Name>: (
                        (<square_size>),        # with default process_method with square size
                        (<width>, <height>),    # with default process_method with width/height
                        (<width>, <height>, <method_name>), 
                        (<width>, <height>, <method_name>, <method_options>), 
                    ),
                    <Name>: (
                        (<width>, <height>, <method_name>, <method_options>), 
                        (<width>, <height>, <method_name>, <method_options>), 
                        (<width>, <height>, <method_name>, <method_options>), 
                    ),
                }

            ``Name`` is a name of thumbnail. ``None`` or '' for original image.

            ``width`` and ``height`` is used in process method. Some process method
            have to be set this value ``None``

            ``method_name`` is a name of method or process_method. You can use a
            string name registered in settings.THUMBNAILFIELD_PROCESS_METHOD_TABLE

            ``method_options`` is a dictionary instance used in particular method.
            for example, ``crop`` method required ``left`` and ``upper`` options to
            process.
        """
        patterns = patterns or []
        if '' in patterns:
            patterns[None] = patterns['']
            del patterns['']
        self.patterns = patterns
        super(ThumbnailField, self).__init__(verbose_name, name, width_field, height_field, **kwargs) 
