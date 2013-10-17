# -*- coding: utf-8 -*-
 
from django.forms import ModelForm, Form, fields, PasswordInput
from models import UserProfile
 
class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', )
        
        
class RegisterForm(Form):
    fio = fields.CharField(label=u'ФИО')
    email = fields.EmailField(label=u'email')
    password_1 = fields.CharField(label=u'пароль 1', widget=PasswordInput)
    password_2 = fields.CharField(label=u'пароль 2', widget=PasswordInput)
    
        
class RegisterOptForm(ModelForm):
    
    class Meta:
        model = UserProfile
        exclude = ('user', )
    
    fio = fields.CharField(label=u'ФИО')
    email = fields.EmailField(label=u'email')
    password_1 = fields.CharField(label=u'пароль 1', widget=PasswordInput)
    password_2 = fields.CharField(label=u'пароль 2', widget=PasswordInput)
    phone = fields.CharField(label=u'телефон')
    city = fields.CharField(label=u'город')
    organization = fields.CharField(label=u'организация')
    address = fields.CharField(label=u'адрес')