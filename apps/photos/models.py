# -*- coding: utf-8 -*-
from django.db import models


class Photo(models.Model):
    """Uploaded photo."""
    image = models.ImageField(upload_to='photos')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    # def image_img(self):
    #     """Thumbnail."""
    #     if self.image:
    #         return u'<img src="%s" />' % self.image.url_125x125
    #     else:
    #         return '(No photo)'
    # image_img.short_description = 'Thumb'
    # image_img.allow_tags = True
