# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(models.Photo, PhotoAdmin)
