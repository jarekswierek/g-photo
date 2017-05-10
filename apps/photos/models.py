# -*- coding: utf-8 -*-
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import BarChart

from django.db import models
from django.conf import settings

from . import fields, validators, concepts, threads, thumbnails


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
        """Photo concepts chart.
        """
        if self.concepts:
            data = SimpleDataSource(data=self.concepts['data'])
            options = {'title': '', 'isStacked': 'absolute'}
            chart = BarChart(data, options=options)
            return chart.as_html()
        else:
            return '(Waiting for an API response. It may take a few seconds. ' \
                   'Refresh page to see results.)'

    concepts_chart.short_description = 'Concepts'
    concepts_chart.allow_tags = True

    def image_tag(self):
        """Image tag.
        """
        if self.image:
            return '<img src="{src}" />'.format(src=self.image.url)
        else:
            return settings.NO_PHOTO_MSG

    image_tag.short_description = 'Preview'
    image_tag.allow_tags = True

    def thumb_tag(self):
        """Thumbnail tag.
        """
        if self.thumbnail:
            return '<img src="{src}" />'.format(src=self.thumbnail.url)
        else:
            return settings.NO_PHOTO_MSG

    thumb_tag.short_description = 'Thumb'
    thumb_tag.allow_tags = True

    def save(self):
        """Save photo with thumbnail.
        """
        self.create_thumbnail()
        super(Photo, self).save()
        threads.run_background_task(self.save_photo_concepts)

    def create_thumbnail(self):
        """Create photo thumbnail.
        """
        if not self.image.file or not hasattr(self.image.file, 'content_type'):
            return None
        filename, thumb = thumbnails.get_thumbnail(self.image)
        self.thumbnail.save(filename, thumb, save=False)

    def get_photo_concepts(self):
        """Get photo concepts returned by API.
        """
        return concepts.photo_concepts(self.image)

    def save_photo_concepts(self):
        """Save photo concepts in database.
        """
        data = self.get_photo_concepts()
        if data:
            try:
                photo_concepts = data['outputs'][0]['data']['concepts']
            except (KeyError, IndexError):
                photo_concepts = []
            if photo_concepts:
                header = [['concept', 'probability']]
                concepts_list = [[elem['name'], float(elem['value'])]
                                 for elem in photo_concepts]
                self.concepts = {'data': header + concepts_list}
                self.save()
