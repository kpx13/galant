# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.template import Context, Template

from catalog.models import Item, Size

class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name=u'пользователь')
    item = models.ForeignKey(Item, verbose_name=u'товар')
    size = models.ForeignKey(Size, blank=True, null=True, verbose_name=u'размер')
    count = models.IntegerField(default=1, verbose_name=u'количество')
    date = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'дата добавления')
    
    
    class Meta:
        verbose_name = u'товар в корзине'
        verbose_name_plural = u'товары в корзине'
        ordering = ['-date']
        
    def __unicode__(self):
        return self.item.name
    
    @staticmethod
    def add_to_cart(user, item, size, count=1):
        alr = Cart.objects.filter(user=user, item=item, size=Size.objects.get(name=size))
        if len(alr) == 0:
            Cart(user=user, item=Item.get(item), size=Size.objects.get(name=size), count=count).save()
        else:
            alr[0].count = alr[0].count + count
            alr[0].save()
    
    @staticmethod     
    def update(user, dict_): 
        for d in dict_:
            Cart(user=user, item=d['item'], count=d['count'], size=Size.objects.get(name=d['size'])).save()
    
    @staticmethod
    def set_count(user, item, size, count):
        if count <= 0:
            Cart.objects.filter(user=user, item=item, size=Size.objects.get(name=size)).delete()
        else: 
            alr = Cart.objects.filter(user=user, item=item, size=Size.objects.get(name=size))[0]
            alr.count = count 
            alr.save()
    
    @staticmethod
    def count_plus(user, item, size):
        alr = Cart.objects.filter(user=user, item=item, size=Size.objects.get(name=size))[0]
        alr.count += 1 
        alr.save()
            
    
    @staticmethod
    def count_minus(user, item, size):
        alr = Cart.objects.filter(user=user, item=item, size=Size.objects.get(name=size))[0]
        if alr.count <= 1:
            alr.delete()
            return
        alr.count -= 1 
        alr.save()
            
    @staticmethod
    def del_from_cart(user, item, size):
        Cart.objects.filter(user=user, item=item, size=Size.objects.get(name=size)).delete()
    
    @staticmethod    
    def clear(user):
        Cart.objects.filter(user=user).delete()
    
    @staticmethod
    def get_content(user):
        cart = list(Cart.objects.filter(user=user))
        res = []
        for c in cart:
            res.append({'item': c.item,
                        'size': c.size.name,
                        'count': c.count,
                        'sum': c.item.price * c.count})
        return res
    
    @staticmethod
    def present_item(user, item):
        cart = list(Cart.objects.filter(user=user, item=item))
        res = []
        for c in cart:
            res.append({'item': c.item,
                        'size': c.size.name,
                        'count': c.count,
                        'sum': c.item.price * c.count})
        return res
    
    @staticmethod
    def get_count(user, item, size):
        cart = list(Cart.objects.filter(user=user, item=item, size=Size.objects.get(name=size)))
        if len(cart) > 0:
            return cart[0].count
        else:
            return 0
    
    @staticmethod
    def get_goods_count_and_sum(user):
        cart = Cart.get_content(user)
        return (sum([x['count'] for x in cart]), sum([x['count'] * x['item'].price for x in cart]))


DELIVERY_TYPE = (('post', u'Почта России'),
                 ('pickpoint', u'Пункты выдачи PickPoint'),
                 ('ems', u'EMS Почта России (экспресс почта)'),)

class Order(models.Model):
    user = models.ForeignKey(User, verbose_name=u'пользователь')
    date = models.DateTimeField(default=datetime.datetime.now, verbose_name=u'дата заказа')
    comment = models.TextField(blank=True, verbose_name=u'комментарий')
    delivery = models.CharField(choices=DELIVERY_TYPE, max_length=10, blank=True, verbose_name=u'способ доставки')
    is_commit = models.BooleanField(blank=True, default=False, verbose_name=u'заказ отправлен')
    
    class Meta:
        verbose_name = u'заказ'
        verbose_name_plural = u'заказы'
        ordering = ['-date']
    
    def __unicode__(self):
        return str(self.date)
    
    def get_count(self):
        return sum([x.count for x in OrderContent.get_content(self)])
    
    def get_sum(self):
        return sum([x.count * x.item.price for x in OrderContent.get_content(self)])
    
    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
    
    def send(self):
        OrderContent.move_from_cart(self.user, self)
        self.is_commit = True
        self.save()
    
    @staticmethod
    def get_recent(user):
        try:
            return Order.objects.filter(user=user, is_commit=False)[0]
        except:
            return None # ошибка, необходимо вернуться на шаг назад
        
    @staticmethod
    def get_or_create(user):
        try:
            return Order.objects.filter(user=user, is_commit=False)[0]
        except:
            u = Order(user=user)
            u.save()
            return u
                
class OrderContent(models.Model):
    order = models.ForeignKey(Order, verbose_name=u'заказ', related_name='content')
    item = models.ForeignKey(Item, verbose_name=u'товар')
    size = models.ForeignKey(Size, blank=True, null=True, verbose_name=u'размер')
    count = models.IntegerField(default=1, verbose_name=u'количество')
        
    def __unicode__(self):
        return self.item.name
    
    @staticmethod
    def add(order, item, count, size=None):
        OrderContent(order=order, item=item, size=size, count=count).save()
        
    @staticmethod
    def move_from_cart(user, order):
        cart_content = Cart.get_content(user)
        for c in cart_content:
            OrderContent.add(order, c['item'], c['count'], Size.objects.get(name=c['size']))
        Cart.clear(user) 
        
    @staticmethod
    def get_content(order):
        return list(OrderContent.objects.filter(order=order))
    