# -*- coding: utf-8 -*-
import os
from io import BytesIO

from PIL import Image

from django.db import models
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from .validators import validate_photo_extension
from .exceptions import PhotoException


class Photo(models.Model):
    """Uploaded photo.
    """
    image = models.ImageField(
        upload_to='photos', validators=[validate_photo_extension])
    name = models.CharField(max_length=255)
    thumbnail = models.ImageField(
        upload_to='thumbs', max_length=500, blank=True, null=True)

    def thumb(self):
        """Thumbnail as html img element.
        """
        if self.thumbnail:
            return '<img src="%s" />' % self.thumbnail.url
        else:
            return settings.NO_PHOTO_MSG

    thumb.short_description = 'Thumb'
    thumb.allow_tags = True

    def create_thumbnail(self):
        """Method for creating image thumbnail.
        """
        if not self.image.file or not hasattr(self.image.file, 'content_type'):
            return None

        content_type = self.image.file.content_type
        if content_type == 'image/jpeg':
            pil_type = 'jpeg'
            file_extension = 'jpg'
        elif content_type == 'image/png':
            pil_type = 'png'
            file_extension = 'png'
        else:
            raise PhotoException('Content type of file not found.')

        # Open original photo which we want to thumbnail using PIL's Image
        image = Image.open(BytesIO(self.image.read()))

        image.thumbnail(settings.THUMBNAIL_SIZE, Image.ANTIALIAS)

        # Save the thumbnail
        temp_handle = BytesIO()
        image.save(temp_handle, pil_type)
        temp_handle.seek(0)

        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(
            os.path.split(self.image.name)[-1],
            temp_handle.read(),
            content_type=content_type
        )
        # Save SimpleUploadedFile into image field
        filename = '{0}_thumbnail.{1}'.format(
            os.path.splitext(suf.name)[0], file_extension)
        self.thumbnail.save(filename, suf, save=False)

    def save(self):
        """Save photo with thumbnail.
        """
        self.create_thumbnail()
        super(Photo, self).save()
