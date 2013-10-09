# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Brand, Category, Color, Image, Item, Material

class ImageInline(admin.StackedInline): 
    model = Image
    extra = 3
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'order')
    
class ItemAdmin(admin.ModelAdmin):
    inlines = [ ImageInline, ]
    list_display = ('name', 'category', 'price',  'stock')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Material)
admin.site.register(Item, ItemAdmin)