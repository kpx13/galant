# -*- coding: utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField
import pytils
from dashboard import string_with_title

class Page(models.Model):
    title = models.CharField(max_length=256, verbose_name=u'заголовок')
    content = RichTextField(blank=True, verbose_name=u'контент')
    slug = models.SlugField(verbose_name=u'слаг', blank=True, unique=True, help_text=u'заполнять не нужно')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.title)
        super(Page, self).save(*args, **kwargs)
    
    @staticmethod
    def get_page_by_slug(page_name):
        try:
            page = Page.objects.get(slug=page_name)
            return {'title': page.title,
                    'content': page.content
                    }
        except:
            return None
        
    
    class Meta:
        verbose_name = u'статическая страница'
        verbose_name_plural = u'статические страницы'
        app_label = string_with_title("pages", u"Страницы")
        
    def __unicode__(self):
        return self.slug