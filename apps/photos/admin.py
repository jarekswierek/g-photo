# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models


class PhotoAdmin(admin.ModelAdmin):
    """Photos admin views.
    """
    list_display = ('thumb', 'name',)
    readonly_fields = ('thumbnail',)


admin.site.register(models.Photo, PhotoAdmin)
