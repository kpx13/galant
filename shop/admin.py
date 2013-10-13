# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Cart, Order, OrderContent

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'count', 'date')
    search_fields = ('item', )

class ContentInline(admin.TabularInline): 
    list_display = ('item', 'size', 'count')
    model = OrderContent
    extra = 2

class OrderAdmin(admin.ModelAdmin):
    inlines = [ ContentInline, ]
    list_display = ('user', 'date')
    search_fields = ('user', )

admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)