# -*- coding: utf-8 -*-

from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from ckeditor.fields import RichTextField
import pytils

class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True, verbose_name=u'название')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'родитель')
    order = models.IntegerField(null=True, blank=True, default=100, verbose_name=u'порядок сортировки')
    slug = models.SlugField(verbose_name=u'слаг', unique=True, blank=True, help_text=u'заполнять не нужно')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    
    @staticmethod
    def get_by_slug(page_name):
        try:
            return Category.objects.get(slug=page_name)
        except:
            return None
        
    class Meta:
        verbose_name = u'категория'
        verbose_name_plural = u'категории'
        ordering=['order']
    
    def __unicode__(self):
        return self.name
    
    @staticmethod
    def get(id_):
        try:
            return Category.objects.get(id=id_)
        except:
            return None
        
class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=u'название')
    slug = models.SlugField(verbose_name=u'слаг', unique=True, blank=True, help_text=u'заполнять не нужно')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.name)
        super(Brand, self).save(*args, **kwargs)
    
    @staticmethod
    def get_by_slug(page_name):
        try:
            return Brand.objects.get(slug=page_name)
        except:
            return None
        
    class Meta:
        verbose_name = u'бренд'
        verbose_name_plural = u'бренды'
        ordering=['id']
    
    def __unicode__(self):
        return self.name
    
class Color(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=u'название')
        
    class Meta:
        verbose_name = u'цвет'
        verbose_name_plural = u'цвета'
        ordering=['name']
    
    def __unicode__(self):
        return self.name
    
class Material(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=u'название')
        
    class Meta:
        verbose_name = u'материал'
        verbose_name_plural = u'материалы'
        ordering=['name']
    
    def __unicode__(self):
        return self.name
    
class Size(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=u'название')
        
    class Meta:
        verbose_name = u'размер'
        verbose_name_plural = u'размеры'
        ordering=['name']
    
    def __unicode__(self):
        return self.name
    
class Item(models.Model):
    category = models.ForeignKey(Category, verbose_name=u'категория', related_name='item')
    brand = models.ForeignKey(Brand, verbose_name=u'категория', related_name='item')
    color = models.ForeignKey(Color, blank=True, verbose_name=u'категория', related_name='item')
    material = models.ForeignKey(Material, blank=True, verbose_name=u'категория', related_name='item')
    size = models.ForeignKey(Size, blank=True, verbose_name=u'категория', related_name='item')
    name = models.CharField(max_length=512, verbose_name=u'название')
    price = models.FloatField(verbose_name=u'цена')
    price_new = models.FloatField(verbose_name=u'новая цена (для акций)')
    description = RichTextField(default=u'', verbose_name=u'описание')
    stock = models.IntegerField(default=0, blank=True, verbose_name=u'в наличии')
    order = models.IntegerField(null=True, blank=True, default=100, verbose_name=u'порядок сортировки')

    @staticmethod
    def get(id_):
        try:
            return Item.objects.get(id=id_)
        except:
            return None
    
    @staticmethod
    def get_home():
        return Item.objects.filter(at_home=True, in_archive=False)
    
    def same_category(self):
        return Item.objects.filter(category=self.category, in_archive=False).exclude(id = self.id)
    
    def same_collection(self):
        return Item.objects.filter(collection=self.collection, in_archive=False).exclude(id = self.id)
    
    def get_path(self):
        path = [self.category]
        while path[0].parent:
            path.insert(0, path[0].parent)
        return path
    
    class Meta:
        verbose_name = u'товар'
        verbose_name_plural = u'товары'
        ordering=['order']
        
    def __unicode__(self):
        return self.name
    
class Image(models.Model):
    item = models.ForeignKey(Item, verbose_name=u'товар', related_name='image')
    image = models.ImageField(upload_to='uploads/items', max_length=256, blank=True, verbose_name=u'изображение')
    order = models.IntegerField(null=True, blank=True, default=100, verbose_name=u'порядок сортировки')

    @staticmethod
    def get(id_):
        try:
            return Item.objects.get(id=id_)
        except:
            return None
    
    class Meta:
        verbose_name = u'изображение'
        verbose_name_plural = u'изображения'
        ordering=['order']
        
    def __unicode__(self):
        return str(self.item) + ' ' + str(self.id) 
    
    