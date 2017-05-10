# -*- coding: utf-8 -*-
import os
from io import BytesIO

from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from . import exceptions


def get_thumbnail(photo):
    """Get thumbnail from given photo.
    """
    content_type = photo.file.content_type
    if content_type == 'image/jpeg':
        pil_type = 'jpeg'
        file_extension = 'jpg'
    elif content_type == 'image/png':
        pil_type = 'png'
        file_extension = 'png'
    else:
        raise exceptions.PhotoException('Content type of file not found.')

    # Open original photo which we want to thumbnail using PIL's Image
    image = Image.open(BytesIO(photo.read()))

    image.thumbnail(settings.THUMBNAIL_SIZE, Image.ANTIALIAS)

    # Save the thumbnail
    temp_handle = BytesIO()
    image.save(temp_handle, pil_type)
    temp_handle.seek(0)

    # Save image to a SimpleUploadedFile which can be saved into
    # ImageField
    thumb = SimpleUploadedFile(
        os.path.split(photo.name)[-1],
        temp_handle.read(),
        content_type=content_type
    )
    # Save SimpleUploadedFile into image field
    filename = '{0}_thumbnail.{1}'.format(
        os.path.splitext(thumb.name)[0], file_extension)
    return filename, thumb
