# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import RequestContext

from request.forms import RequestForm
from pages.models import Page
from news.models import NewsItem
from catalog.models import Item, Category, Collection
from shop.models import Cart, Order

class SessionFavoritesWorking(object):
    def __init__(self, request):
        self.__request = request
        
    def var(self, item):
        return 'favorites_' + str(item)
        
    def add_to_favorites(self, item):
        self.__request.session[self.var(item)] = True
    
    def del_favorites(self, item):
        del self.__request.session[self.var(item)]
    
    def favorites_check(self, item):
        return self.__request.session.get(self.var(item), False)
    
    def get_items(self):
        return [Item.get(int(i[10:])) for i in self.__request.session.keys() if i.startswith('favorites_')]


class SessionCartWorking(object):
    def __init__(self, request):
        self.__request = request
        
    def var(self, item):
        return 'cart_' + str(item)
        
    def add_to_cart(self, cap, item):
        self.__request.session[self.var(item)] = 1
    
    def del_from_cart(self, cap, item):
        del self.__request.session[self.var(item)]

    def get_content(self, cap):
        res = []
        for i in self.__request.session.keys():
            if i.startswith('cart_'):
                res.append({'item': Item.get(int(i[5:])),
                     'count': int(self.__request.session[i])})
        return res
    
    def pop_content(self):
        res = []
        for i in self.__request.session.keys():
            if i.startswith('cart_'):
                res.append({'item': Item.get(int(i[5:])),
                     'count': int(self.__request.session[i])})
                del self.__request.session[i]
        return res
    
    def get_goods_count_and_sum(self, cap):
        cart = self.get_content(cap)
        return (sum([x['count'] for x in cart]), sum([x['count'] * x['item'].price for x in cart]))
    
    def count_plus(self, cap, item):
        self.__request.session[self.var(item)] += 1
        
    def count_minus(self, cap, item):
        if self.__request.session[self.var(item)] <= 1:
            self.del_from_cart(cap, item)
        else:
            self.__request.session[self.var(item)] -= 1
    
    