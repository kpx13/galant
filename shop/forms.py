# -*- coding: utf-8 -*-
 
from django.forms import ModelForm, Form, fields, PasswordInput
from models import Order
        
class OrderForm(ModelForm):
    class Meta:
        model = Order
                
        
class Step2Form(Form):
    fio = fields.CharField(label=u'ФИО')
    city = fields.CharField(label=u'город', required=False)
    index = fields.CharField(label=u'индекс')
    phone = fields.CharField(label=u'телефон')
    email = fields.EmailField(label=u'email')
    
    