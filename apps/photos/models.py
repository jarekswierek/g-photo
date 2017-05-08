# -*- coding: utf-8 -*-
import os
from io import BytesIO

from PIL import Image

from django.db import models
from django.core.files.uploadedfile import SimpleUploadedFile

from .validators import validate_photo_extension


class Photo(models.Model):
    """Uploaded photo.
    """
    image = models.ImageField(
        upload_to='photos', validators=[validate_photo_extension])
    name = models.CharField(max_length=255)
    thumbnail = models.ImageField(
        upload_to='thumbs', max_length=500, blank=True, null=True)

    def thumb(self):
        if self.thumbnail:
            return u'<img src="%s" />' % self.thumbnail.url
        else:
            return '(No photo)'
    thumb.short_description = 'Thumb'
    thumb.allow_tags = True

    def create_thumbnail(self):
        if not self.image:
            return

        THUMBNAIL_SIZE = (90, 90)
        DJANGO_TYPE = self.image.file.content_type

        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'

        # Open original photo which we want to thumbnail using PIL's Image
        image = Image.open(BytesIO(self.image.read()))

        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        # Save the thumbnail
        temp_handle = BytesIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(
            os.path.split(self.image.name)[-1],
            temp_handle.read(),
            content_type=DJANGO_TYPE
        )
        # Save SimpleUploadedFile into image field
        filename = '{0}_thumbnail.{1}'.format(
            os.path.splitext(suf.name)[0], FILE_EXTENSION)
        self.thumbnail.save(filename, suf, save=False)

    def save(self):
        self.create_thumbnail()
        super(Photo, self).save()
