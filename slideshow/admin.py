# -*- coding: utf-8 -*-
from django.contrib import admin
import models

class SliderAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'sort_parameter')
    ordering = ('sort_parameter', )
    
admin.site.register(models.Slider, SliderAdmin)