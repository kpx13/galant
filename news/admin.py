# -*- coding: utf-8 -*-
from django.contrib import admin
from models import NewsItem, NewsItemPhoto

class PhotoInline(admin.TabularInline): 
    list_display = ('image', )
    model = NewsItemPhoto
    extra = 10
    
class ItemAdmin(admin.ModelAdmin):
    inlines = [ PhotoInline, ]
    list_display = ('name', )
    

admin.site.register(NewsItem, ItemAdmin)