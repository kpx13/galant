# -*- coding: utf-8 -*-
from django.db import models

class Slider(models.Model):
    image = models.ImageField(upload_to= 'uploads/slider', max_length=256, verbose_name=u'картинка')
    sort_parameter = models.IntegerField(default=0, blank=True, verbose_name=u'порядок сортировки', help_text=u'№ слайдера: 1й, 2й .. 5й')
    
    class Meta:
        verbose_name = 'слайдер'
        verbose_name_plural = 'слайдер'
        ordering = ['sort_parameter']
        
    
    def __unicode__(self):
        return str(self.id)