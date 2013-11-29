# -*- coding: utf-8 -*-

from catalog.models import Item

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
        if size and size != 'None':
            return  '_'.join(['cart', str(item), str(size)])
        else:
            return  '_'.join(['cart', str(item), '0'])
        
    def add_to_cart(self, cap, item, size):
        if self.var(item, size) in self.__request.session.keys():
            self.__request.session[self.var(item, size)] += 1
        else:
            self.__request.session[self.var(item, size)] = 1 
    
    def del_from_cart(self, cap, item, size):
	    del self.__request.session[self.var(item, size)]
        
    def get_count(self, cap, item, size):
        return self.__request.session[self.var(item, size)]
    
    def get_price(self, cap, item):
        opt = cap.is_authenticated() and cap.get_profile().is_opt
        if opt: 
            return item.price_opt
        else:
            return item.price
    
    def get_content(self, cap):
        res = []
        
        for i in self.__request.session.keys():
            if i.startswith('cart_'):
                item, size = get_item_and_size(i[5:])
                item = Item.get(int(item))
                if size == '0': size = None
                res.append({'item': item,
                            'size': size,
                            'count': int(self.__request.session[i]),
                            'price': self.get_price(cap, item),
                            'sum': int(self.__request.session[i]) * self.get_price(cap, item)})
        return res
    
    def present_item(self, cap, item):
        res = []
        for i in self.__request.session.keys():
            if i.startswith('cart_' + str(item)):
                item, size = get_item_and_size(i[5:])
                if size == '0': size = None
                item = Item.get(int(item))
                res.append({'item': item,
                            'size': size,
                            'count': int(self.__request.session[i]),
                            'sum': int(self.__request.session[i]) * self.get_price(cap, item)})
        return res
    
    def pop_content(self):
        res = []
        for i in self.__request.session.keys():
            if i.startswith('cart_'):
                item, size = get_item_and_size(i[5:])
                if size == '0': size = None
                res.append({'item': Item.get(int(item)),
                            'size': size,
                            'count': int(self.__request.session[i])})
                del self.__request.session[i]
        return res
    
    def get_goods_count_and_sum(self, cap):
        cart = self.get_content(cap)
        return (sum([x['count'] for x in cart]), sum([x['count'] * self.get_price(cap, x['item']) for x in cart]))
    
    def count_plus(self, cap, item, size):
        self.__request.session[self.var(item, size)] += 1
        
    def count_minus(self, cap, item, size):
        if self.__request.session[self.var(item, size)] <= 1:
            self.del_from_cart(cap, item, size)
        else:
            self.__request.session[self.var(item, size)] -= 1
            
    def set_count(self, cap, item, size, count):
        count= int(count)
        
        if count <= 0:
            self.del_from_cart(cap, item, size)
        else:
            self.__request.session[self.var(item, size)] = count
    
    
