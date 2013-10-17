# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from dashboard import string_with_title

import config
from livesettings import config_value
from django.template import Context, Template
from django.conf import settings
from django.core.mail import send_mail

def sendmail(subject, body, to_email=config_value('MyApp', 'EMAIL')):
    mail_subject = ''.join(subject)
    send_mail(mail_subject, body, settings.DEFAULT_FROM_EMAIL,
        [to_email])


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', verbose_name=u'пользователь')
    fio = models.CharField(max_length=256, verbose_name=u'ФИО')
    phone = models.CharField(max_length=128, blank=True, verbose_name=u'телефон')
    index = models.CharField(max_length=25, blank=True,verbose_name=u'индекс')
    city = models.CharField(max_length=100, blank=True,verbose_name=u'город')
    street = models.CharField(max_length=256, blank=True,verbose_name=u'улица')
    house = models.CharField(max_length=25, blank=True,verbose_name=u'дом, квартира')
    
    is_opt = models.BooleanField(blank=True, verbose_name=u'это оптовик')
    organization = models.CharField(max_length=20,blank=True, verbose_name=u'организация')
    address = models.CharField(max_length=20, blank=True, verbose_name=u'адрес ТЦ')
    

    class Meta:
        verbose_name = 'профиль пользователя'
        verbose_name_plural = 'профили пользователей'
        app_label = string_with_title("users", u"Пользователи")
    
    def __unicode__ (self):
        return str(self.user.username)
    
    
    def send(self):
        
        subject=u'Поступила новая заявка от оптовика',
        body_templ=u"""
    Контактное лицо: {{ up.fio }}
    Организация: {{ up.organization }}
    Адрес: {{ up.address }}
    
    Если Вы хотите подтвердить профиль оптовика, это можно сделать здесь: {{ site }}admin/auth/user/{{ up.user.id }}/
    
    """
        body = Template(body_templ).render(Context({'up': self, 'site': 'http://galant.webgenesis.ru/'}))
        sendmail(subject, body)    
    
        
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
