# -*- coding: utf-8 -*-
from django.contrib import admin

from . import models


class PhotoAdmin(admin.ModelAdmin):
    """Photos admin views.
    """
    list_display = ('thumb_tag', 'name',)
    readonly_fields = ('image_tag',)
    fields = ('name', 'image')
    update_fields = ('image_tag', 'name', 'image')

    def get_form(self, request, obj=None, **kwargs):
        """Set update fields on photo edit.
        """
        if obj and obj.pk:
            self.fields = self.update_fields
        return super(PhotoAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(models.Photo, PhotoAdmin)
