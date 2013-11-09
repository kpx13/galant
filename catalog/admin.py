# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Brand, Category, Color, Image, Item, Material, Size

class ImageInline(admin.StackedInline): 
    model = Image
    extra = 3
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'parent', 'order')

class SizeAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'order')

    
class ItemAdmin(admin.ModelAdmin):
    inlines = [ ImageInline, ]
    list_display = ('art', 'category', 'price', 'price_old', 'price_opt', 'season', 'at_home')
    search_fields = ['art', ]
    list_filter = ('category', )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Material)
admin.site.register(Size, SizeAdmin)
admin.site.register(Item, ItemAdmin)
