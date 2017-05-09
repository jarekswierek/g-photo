# -*- coding: utf-8 -*-
import os
import json
from io import BytesIO

from PIL import Image
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from clarifai.rest.client import ApiError
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import BarChart

from django.db import models
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from . import fields, validators, exceptions


class Photo(models.Model):
    """Uploaded photo.
    """
    image = models.ImageField(
        upload_to='photos', validators=[validators.validate_photo_extension])
    name = models.CharField(max_length=255)
    thumbnail = models.ImageField(
        upload_to='thumbs', max_length=500, blank=True, null=True)
    concepts = fields.JSONField(blank=True, null=True)

    def concepts_chart(self):
        # data = [
        #     ['concept', 'probably'],
        #     ['dog', 0.4],
        #     ['cat', 0.7],
        #     ['animal', 0.99],
        # ]
        data = []
        chart = BarChart(SimpleDataSource(data=data), options={'title': ''})
        return chart.as_html()

    concepts_chart.short_description = 'Concepts'
    concepts_chart.allow_tags = True

    def image_tag(self):
        """Image tag.
        """
        if self.image:
            return u'<img src="%s" />' % self.image.url
        else:
            return settings.NO_PHOTO_MSG

    image_tag.short_description = 'Preview'
    image_tag.allow_tags = True

    def thumb_tag(self):
        """Thumbnail tag.
        """
        if self.thumbnail:
            return '<img src="%s" />' % self.thumbnail.url
        else:
            return settings.NO_PHOTO_MSG

    thumb_tag.short_description = 'Thumb'
    thumb_tag.allow_tags = True

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
            raise exceptions.PhotoException('Content type of file not found.')

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
        self.set_photo_concepts()
        super(Photo, self).save()

    def vision(self):
        with open('api_keys.json') as data_file:
            credentials = json.load(data_file)
        app_id = credentials['api_key']
        app_secret = credentials['api_secret']
        app = ClarifaiApp(app_id=app_id, app_secret=app_secret)
        model = app.models.get('general-v1.3')
        image = ClImage(file_obj=BytesIO(self.image.read()))
        try:
            result = model.predict([image])
        except ApiError:
            result = []
        return result

    def set_photo_concepts(self):
        result = self.vision()
        try:
            status_code = result['status']['code']
        except KeyError:
            pass
        else:
            if status_code == 10000:
                try:
                    concepts = result['outputs'][0]['data']['concepts']
                except (KeyError, IndexError):
                    concepts = []
                concepts_list = [{'name': elem['name'], 'value': elem['value']}
                                 for elem in concepts]
                self.concepts = {'data': concepts_list}
