# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from models import UserProfile

class UserProfileInline(admin.StackedInline): 
    model = UserProfile
    extra = 1

class ExtUserAdmin(UserAdmin):
    inlines = [ UserProfileInline, ]
    list_display = UserAdmin.list_display + ('is_active',)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('fio', 'city', 'is_opt')


admin.site.unregister(User)
admin.site.register(User, ExtUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)