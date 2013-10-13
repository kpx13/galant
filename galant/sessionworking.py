# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import RequestContext


from pages.models import Page
from news.models import NewsItem
from catalog.models import Item, Category, Size
from shop.models import Cart, Order

def get_item_and_size(is_str):
    res = is_str.split('_')
    if len(res) > 1:
        return (res[0], res[1])
    else:
        return is_str, 1

class SessionCartWorking(object):
    def __init__(self, request):
        self.__request = request
        
    def var(self, item, size):
        return  '_'.join(['cart', str(item), str(size)])
        
    def add_to_cart(self, cap, item, size):
        if self.var(item, size) in self.__request.session.keys():
            self.__request.session[self.var(item, size)] += 1
        else:
            self.__request.session[self.var(item, size)] = 1 
    
    def del_from_cart(self, cap, item, size):
        del self.__request.session[self.var(item, size)]
        
    def get_count(self, cap, item, size):
        return self.__request.session[self.var(item, size)]
    
    def get_content(self, cap):
        res = []
        
        for i in self.__request.session.keys():
            if i.startswith('cart_'):
                item, size = get_item_and_size(i[5:])
                item = Item.get(int(item))
                res.append({'item': item,
                            'size': size,
                            'count': int(self.__request.session[i]),
                            'sum': int(self.__request.session[i]) * item.price})
        return res
    
    def pop_content(self):
        res = []
        for i in self.__request.session.keys():
            if i.startswith('cart_'):
                item, size = get_item_and_size(i[5:])
                res.append({'item': Item.get(int(item)),
                            'size': size,
                            'count': int(self.__request.session[i])})
                del self.__request.session[i]
        return res
    
    def get_goods_count_and_sum(self, cap):
        cart = self.get_content(cap)
        return (sum([x['count'] for x in cart]), sum([x['count'] * x['item'].price for x in cart]))
    
    def count_plus(self, cap, item, size):
        self.__request.session[self.var(item, size)] += 1
        
    def count_minus(self, cap, item, size):
        if self.__request.session[self.var(item, size)] <= 1:
            self.del_from_cart(cap, item, size)
        else:
            self.__request.session[self.var(item, size)] -= 1
            
    def set_count(self, cap, item, size, count):
        print count
        count= int(count)
        
        if count <= 0:
            self.del_from_cart(cap, item, size)
        else:
            self.__request.session[self.var(item, size)] = count
    
    