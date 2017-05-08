# -*- coding: utf-8 -*-
from django.db import models


class Photo(models.Model):
    """Uploaded photo."""
    image = models.ImageField(upload_to='photos')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
