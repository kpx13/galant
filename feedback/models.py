# -*- coding: utf-8 -*-
from django.db import models
from pytils import dt
from dashboard import string_with_title

class Feedback(models.Model):
    name  = models.CharField(u'Имя', max_length=255)
    email  = models.CharField(u'Электронная почта', max_length=255)
    msg = models.TextField(u'Вопрос')
    request_date = models.DateTimeField(u'дата заявки', auto_now_add=True)
                    
    class Meta:
        verbose_name = u'сообщение'
        verbose_name_plural = u'вопросы через обратную связь'
        ordering = ['-request_date']
        app_label = string_with_title("feedback", u"Обратная связь")

    def __unicode__(self):
        return u'№ %s от %s' % (self.id, dt.ru_strftime(u"%d %B %Y", self.request_date))
