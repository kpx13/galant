# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import RequestContext

from call_request.forms import CallRequestForm
from pages.models import Page
from news.models import NewsItem
from catalog.models import Category, Brand, Item
#from shop.models import Cart, Order
#from sessionworking import SessionCartWorking, SessionFavoritesWorking

def get_common_context(request):
    c = {}
    c['request_url'] = request.path
    c['user'] = request.user
    c['authentication_form'] = AuthenticationForm()
    c['categories'] = Category.objects.filter(parent=None).extra(order_by = ['id'])
    c['brands'] = Brand.objects.all()
    
    """
    if request.user.is_authenticated():
        c['favorites_working'] = request.user.get_profile()
        c['cart_working'] = Cart
        Cart.update(request.user, SessionCartWorking(request).pop_content())
    else:
        c['favorites_working'] = SessionFavoritesWorking(request)
        c['cart_working'] = SessionCartWorking(request)
    c['cart_count'], c['cart_sum'] = c['cart_working'].get_goods_count_and_sum(request.user)
    """
    c.update(csrf(request))
    return c


def home_page(request):
    c = get_common_context(request)
    c['request_url'] = 'home'
    c['items'] = Item.objects.filter(at_home=True)
    return render_to_response('home.html', c, context_instance=RequestContext(request))

def news(request, slug=None):
    c = get_common_context(request)
    if slug == None:
        c['news'] = NewsItem.objects.all()
        return render_to_response('news.html', c, context_instance=RequestContext(request))
    else:
        c['item'] = NewsItem.get_by_slug(slug)
        return render_to_response('news_item.html', c, context_instance=RequestContext(request))

def category(request, slug):
    c = get_common_context(request)
    c['category'] = Category.get_by_slug(slug)
    items = Item.objects.filter(category__in=c['category'].get_descendants(include_self=True))
    
    if 'sort' in request.GET:
        request.session['catalog_sort'] = request.GET['sort']
    if 'catalog_sort' in request.session:
        items = items.order_by(request.session['catalog_sort'])
        c['sort'] = request.session['catalog_sort']
    else:
        items = items.order_by('name')
        c['sort'] = 'name'
        
    if 'count' in request.GET:
        request.session['catalog_count'] = request.GET['count']
    if 'catalog_count' in request.session:
        items = items[0:request.session['catalog_count']]
        c['count'] = request.session['catalog_count']
    else:
        items = items[0:1]
        c['count'] = 1
    
    c['items'] = items
    return render_to_response('category.html', c, context_instance=RequestContext(request))

def item(request, slug):
    c = get_common_context(request)
    if request.method == 'POST':
        if request.POST['action'] == 'add_in_basket':
            c['cart_working'].add_to_cart(request.user, request.POST['item_id'])
            messages.success(request, u'Товар был добавлен в корзину.')
        elif request.POST['action'] == 'add_to_favorites':
            c['favorites_working'].add_to_favorites(request.POST['item_id'])
        elif request.POST['action'] == 'del_favorites':
            c['favorites_working'].del_favorites(request.POST['item_id'])
        return HttpResponseRedirect(request.get_full_path())
    c['item'] = Item.get_by_slug(slug)
    c['category'] = c['item'].category
    c['same'] = Item.objects.filter(category__in=c['category'].get_descendants(include_self=True))[0:4]
    return render_to_response('item.html', c, context_instance=RequestContext(request))

"""
def cart_page(request):
    c = get_common_context(request)
    if request.method == 'POST':
        if request.POST['action'] == 'del_from_basket':
            c['cart_working'].del_from_cart(request.user, request.POST['item_id'])
            messages.success(request, u'Товар был удален из корзины.')
            return HttpResponseRedirect(request.get_full_path())
        elif request.POST['action'] == 'plus':
            c['cart_working'].count_plus(request.user, request.POST['item_id'])
            return HttpResponseRedirect(request.get_full_path())
        elif request.POST['action'] == 'minus':
            c['cart_working'].count_minus(request.user, request.POST['item_id'])
            return HttpResponseRedirect(request.get_full_path())
        elif request.POST['action'] == 'to_order':
            comment = request.POST['comment']
            deliv = int(request.POST['deliver'])
                
            Order(user=request.user,
                  comment=comment).save()
            messages.success(request, u'Заказ отправлен. Ожидайте звонка.')
            return HttpResponseRedirect('/')
    
    c['items'] = c['cart_working'].get_content(request.user)
    return render_to_response('cart.html', c, context_instance=RequestContext(request))


def order_page(request):
    c = get_common_context(request)
    return render_to_response('order.html', c, context_instance=RequestContext(request))


def news_page(request):
    c = get_common_context(request)
    c['news'] = NewsItem.objects.all()
    return render_to_response('news.html', c, context_instance=RequestContext(request))






def collection_page(request, collection_id):
    c = get_common_context(request)
    c['category'] = Collection.get(collection_id)
    return render_to_response('category.html', c, context_instance=RequestContext(request))

def favorites_page(request):
    c = get_common_context(request)
    c['items'] = c['favorites_working'].get_items()
    return render_to_response('favorites.html', c, context_instance=RequestContext(request))

def search_page(request):
    c = get_common_context(request)
    c['search'] = request.GET.get('search', '')
    c['items_s'] = Item.objects.filter(name__icontains=c['search'])
    c['categories_s'] = Category.objects.filter(name__icontains=c['search'])
    return render_to_response('search.html', c, context_instance=RequestContext(request))

def request_page(request):
    c = get_common_context(request)
    if request.method == 'GET':
        c['request_form'] = RequestForm()
    else:
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
            form = RequestForm()
            messages.success(request, u'Ваш отзыв отправлен. Спасибо.')
            return HttpResponseRedirect('/')
        else:
            c['request_form'] = form
    return render_to_response('request.html', c, context_instance=RequestContext(request))

"""
def other_page(request, page_name):
    c = get_common_context(request)
    try:
        c.update(Page.get_page_by_slug(page_name))
        return render_to_response('page.html', c, context_instance=RequestContext(request))
    except:
        return HttpResponseNotFound('page not found')
        #return render_to_response('base.html', c, context_instance=RequestContext(request))

def login_user(request, c):
    form = AuthenticationForm(request.POST)
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            messages.success(request, u'Вы успешно вошли на сайт.')
            return True
        else:
            c['authentication_form'] = form
            messages.error(request, u'Ваш аккаунт не активирован.')
            return False
    else:
        c['authentication_form'] = form
        messages.error(request, u'Неверный логин или пароль.')
        return False


def logout_user(request):
    auth.logout(request)
