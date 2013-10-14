# -*- coding: utf-8 -*-
 
from django.forms import ModelForm, Form, fields, PasswordInput
from models import Order
        
class OrderForm(ModelForm):
    class Meta:
        model = Order
                
        
class Step3Form(Form):
    fio = fields.CharField(label=u'ФИО')
    phone = fields.CharField(label=u'телефон')
    index = fields.CharField(label=u'индекс')
    city = fields.CharField(label=u'город', required=False)
    street = fields.CharField(label=u'улица')
    house = fields.CharField(label=u'дом, квартира')
    
    