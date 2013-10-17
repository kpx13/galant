# -*- coding: utf-8 -*-
from django.db import models
from pytils import dt

from dashboard import string_with_title
    

class CallRequest(models.Model):
    name  = models.CharField(u'Имя', max_length=255)
    phone  = models.CharField(u'Телефон', max_length=255)
    request_date = models.DateTimeField(u'дата заявки', auto_now_add=True)
                    
    class Meta:
        verbose_name = u'заявка'
        verbose_name_plural = u'заявки на обратный звонок'
        ordering = ['-request_date']
        app_label = string_with_title("call_request", u"Обратный звонок")

    def __unicode__(self):
        return u'№ %s от %s' % (self.id, dt.ru_strftime(u"%d %B %Y", self.request_date))



