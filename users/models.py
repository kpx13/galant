# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', verbose_name=u'пользователь')
    fio = models.CharField(max_length=256, verbose_name=u'ФИО')
    is_opt = models.BooleanField(blank=True, verbose_name=u'это оптовик')
    phone = models.CharField(max_length=20, blank=True, verbose_name=u'телефон')
    city = models.CharField(max_length=20, blank=True,verbose_name=u'город')
    organization = models.CharField(max_length=20,blank=True, verbose_name=u'организация')
    address = models.CharField(max_length=20, blank=True,verbose_name=u'адрес')
    

    class Meta:
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'профили пользователей'
    
    def __unicode__ (self):
        return str(self.user.username)
    
        
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
