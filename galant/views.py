# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponseNotFound, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.forms.util import ErrorList
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime

from call_request.forms import CallRequestForm
from pages.models import Page
from news.models import NewsItem
from catalog.models import Category, Brand, Item, Color, Material
from shop.models import Cart, Order
from sessionworking import SessionCartWorking
from users.forms import RegisterForm, RegisterOptForm, ProfileForm
from feedback.forms import FeedbackForm
from slideshow.models import Slider

NEWS_PAGINATION_COUNT = 10


def get_common_context(request):
    c = {}
    c['request_url'] = request.path
    c['user'] = request.user
    c['authentication_form'] = AuthenticationForm()
    c['categories'] = Category.objects.filter(parent=None).extra(order_by = ['id'])
    c['brands'] = Brand.objects.all()
    c['colors'] = Color.objects.all()
    c['materials'] = Material.objects.all()
    c['news_left'] = NewsItem.objects.all()[0:3]
    c['user_opt'] = request.user.is_authenticated() and request.user.get_profile().is_opt 
    
    if request.user.is_authenticated():
        c['cart_working'] = Cart
        Cart.update(request.user, SessionCartWorking(request).pop_content())
    else:
        c['cart_working'] = SessionCartWorking(request)
    c['cart_count'], c['cart_sum'] = c['cart_working'].get_goods_count_and_sum(request.user)
    c['cart_content'] = c['cart_working'].get_content(request.user)
    c.update(csrf(request))
    
    if request.method == 'POST' and 'action' in request.POST and request.POST['action'] == 'call_request':
        from call_request.forms import CallRequestForm
        crf = CallRequestForm(request.POST)
        if crf.is_valid():
            crf.save()
            c['call_sent'] = True
        else:
            c['crf'] = crf
    
    return c

def reset_catalog(request):
    for i in request.session.keys():
        if i.startswith('catalog_'):
            del request.session[i]


def home_page(request):
    c = get_common_context(request)
    reset_catalog(request)
    c['request_url'] = 'home'
    c['slideshow'] = Slider.objects.all()
    c['items'] = Item.objects.filter(at_home=True)
    return render_to_response('home.html', c, context_instance=RequestContext(request))

def news(request, slug=None):
    c = get_common_context(request)
    reset_catalog(request)
    if slug == None:
        items = NewsItem.objects.all()
        paginator = Paginator(items, NEWS_PAGINATION_COUNT)
        page = int(request.GET.get('page', '1'))
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            items = paginator.page(page)
        except EmptyPage:
            page = paginator.num_pages
            items = paginator.page(page)
        c['page'] = page
        c['page_range'] = paginator.page_range
        if len(c['page_range']) > 1:
            c['need_pagination'] = True
        
        c['news'] = items
        return render_to_response('news.html', c, context_instance=RequestContext(request))
    else:
        c['item'] = NewsItem.get_by_slug(slug)
        return render_to_response('news_item.html', c, context_instance=RequestContext(request))


def filter_items(request, c, items):
    if 'sort' in request.GET:
        request.session['catalog_sort'] = request.GET['sort']
    if 'catalog_sort' in request.session:
        items = items.order_by(request.session['catalog_sort'])
        c['sort'] = request.session['catalog_sort']
    else:
        items = items.order_by('name')
        c['sort'] = 'name'
    
    if 'brand' in request.GET:
        request.session['catalog_brand'] = request.GET['brand']
    if 'catalog_brand' in request.session and request.session['catalog_brand']:
        if Brand.get_by_slug(request.session['catalog_brand']) in c['brands']:
            items = items.filter(brand=Brand.get_by_slug(request.session['catalog_brand']))
            c['brand'] = request.session['catalog_brand']
        else:
            del request.session['catalog_brand']
         
    
    if 'from_price' in request.GET:
        request.session['catalog_from_price'] = request.GET['from_price']
    if 'catalog_from_price' in request.session and request.session['catalog_from_price']:
        items = items.filter(price__gte=int(request.session['catalog_from_price']))
        c['from_price'] = request.session['catalog_from_price']
        
    if 'to_price' in request.GET:
        request.session['catalog_to_price'] = request.GET['to_price']
    if 'catalog_to_price' in request.session and request.session['catalog_to_price']:
        items = items.filter(price__lte=int(request.session['catalog_to_price']))
        c['to_price'] = request.session['catalog_to_price']
        
    if 'season_change' in request.GET:
        request.session['catalog_season'] = request.GET.getlist('season', [])
    if 'catalog_season' in request.session and request.session['catalog_season']:
        items = items.filter(season__in=request.session['catalog_season'])
        c['season'] = request.session['catalog_season']
        
    if 'novelty_sale' in request.GET:
        request.session['catalog_for_sale'] = request.GET.get('for_sale', False)
        request.session['catalog_novelty'] = request.GET.get('novelty', False)
    if 'catalog_for_sale' in request.session and request.session['catalog_for_sale']:
        items = items.exclude(price_old__exact=None)
        c['for_sale'] = True
    if 'catalog_novelty' in request.session and request.session['catalog_novelty']:
        items = items.filter(date__gte=(datetime.datetime.now() - datetime.timedelta(days=7)))
        c['novelty'] = True
    
    if 'color' in request.GET:
        request.session['catalog_color'] = request.GET['color']
    if 'catalog_color' in request.session and request.session['catalog_color']:
        if Color.objects.get(id=int(request.session['catalog_color'])) in c['colors']:
            items = items.filter(color=request.session['catalog_color'])
            c['color'] = int(request.session['catalog_color'])
        else:
            del request.session['catalog_color']
            
        
    if 'material' in request.GET:
        request.session['catalog_material'] = request.GET['material']
    if 'catalog_material' in request.session and request.session['catalog_material']:
        if Material.objects.get(id=int(request.session['catalog_material'])) in c['materials']:
            items = items.filter(material=request.session['catalog_material'])
            c['material'] = int(request.session['catalog_material'])
        else:
            del request.session['catalog_material']
    
    if 'count' in request.GET:
        request.session['catalog_count'] = request.GET['count']
    if 'catalog_count' in request.session:
        c['count'] = request.session['catalog_count']
    else:
        request.session['catalog_count'] = 10
        c['count'] = 10
    
    paginator = Paginator(items, request.session['catalog_count'])
    page = int(request.GET.get('page', '1'))
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        items = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        items = paginator.page(page)
    c['page'] = page
    c['page_range'] = paginator.page_range
    if len(c['page_range']) > 1:
        c['need_pagination'] = True
    
    c['items'] = items
    return c

def category(request, slug):
    c = get_common_context(request)
    if slug:
        c['category'] = Category.get_by_slug(slug)
        items = Item.objects.filter(category__in=c['category'].get_descendants(include_self=True))
    else:
        items = Item.objects.all()
    
    c['brands'] = []
    c['colors'] = []
    c['materials'] = []
    for i in items:
        if i.brand and i.brand not in c['brands']: c['brands'].append(i.brand)
        if i.color and i.color not in c['colors']: c['colors'].append(i.color)
        if i.material and i.material not in c['materials']: c['materials'].append(i.material) 
    
    return render_to_response('category.html', filter_items(request, c, items), context_instance=RequestContext(request))

def brand(request, slug):
    c = get_common_context(request)
    c['brand'] = Brand.get_by_slug(slug)
    items = Item.objects.filter(brand=c['brand'])
    return render_to_response('brand.html', filter_items(request, c, items), context_instance=RequestContext(request))

def item(request, slug):
    c = get_common_context(request)
    if request.method == 'POST':
        if request.POST['action'] == 'add_in_basket':
            sizes = request.POST.getlist('size')
            if sizes:
                for s in sizes:
                    c['cart_working'].add_to_cart(request.user, request.POST['item_id'], s)
            else:
                c['cart_working'].add_to_cart(request.user, request.POST['item_id'], 0)
        return HttpResponseRedirect(request.get_full_path())
    c['item'] = Item.get_by_slug(slug)
    c['category'] = c['item'].category
    c['same'] = Item.objects.filter(category__in=c['category'].get_descendants(include_self=True))[0:4]
    c['in_cart'] = c['cart_working'].present_item(request.user, c['item'].id)
    return render_to_response('item.html', c, context_instance=RequestContext(request))

def cart(request):
    c = get_common_context(request)
    if request.method == 'POST':
        if request.POST['action'] == 'del_from_basket':
            c['cart_working'].del_from_cart(request.user, request.POST['item_id'], request.POST['size'])
            return HttpResponseRedirect(request.get_full_path())
        elif ('set_count' in request.POST) and (int(request.POST['set_count']) != c['cart_working'].get_count(request.user, request.POST['item_id'], request.POST['size'])):
            c['cart_working'].set_count(request.user, request.POST['item_id'], request.POST['size'], request.POST['set_count'])
            return HttpResponseRedirect(request.get_full_path())
        elif request.POST['action'] == 'plus':
            c['cart_working'].count_plus(request.user, request.POST['item_id'], request.POST['size'])
            return HttpResponseRedirect(request.get_full_path())
        elif request.POST['action'] == 'minus':
            c['cart_working'].count_minus(request.user, request.POST['item_id'], request.POST['size'])
            return HttpResponseRedirect(request.get_full_path())
        elif request.POST['action'] == 'to_order':
            comment = request.POST['comment']
            deliv = int(request.POST['deliver'])
                
            Order(user=request.user,
                  comment=comment).save()
            return HttpResponseRedirect('/')
    
    if 'count' in request.GET:
        request.session['catalog_cart_count'] = request.GET['count']
    if 'catalog_cart_count' in request.session:
        c['count'] = request.session['catalog_cart_count']
    else:
        request.session['catalog_cart_count'] = 10
        c['count'] = 10
    
    items = c['cart_working'].get_content(request.user)
    paginator = Paginator(items, request.session['catalog_cart_count'])
    page = int(request.GET.get('page', '1'))
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        items = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        items = paginator.page(page)
    c['page'] = page
    c['page_range'] = paginator.page_range
    if len(c['page_range']) > 1:
        c['need_pagination'] = True
    
    c['items'] = items
    
    return render_to_response('cart.html', c, context_instance=RequestContext(request))

def order(request, step='1'):
    c = get_common_context(request)
    if step == '1':
        if request.user.is_authenticated():
            return HttpResponseRedirect('/order/2/')
        else:
            if request.method == "GET":
                auth_form = AuthenticationForm()
                register_form = RegisterForm()
                c['auth_form'] = auth_form
                c['register_form'] = register_form
                return render_to_response('order_1.html', c, context_instance=RequestContext(request))
            else:
                request.session['is_order'] = True
                return register(request)
    else:
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/order/1/')
    if step == '2':
        c['items'] = c['cart_working'].get_content(request.user)
        return render_to_response('order_2.html', c, context_instance=RequestContext(request))
    elif step == '3':
        from shop.forms import Step3Form
        if request.method == 'GET':
            user_profile = request.user.get_profile()
            form = Step3Form(initial={
                                        'fio': user_profile.fio,
                                        'phone': user_profile.phone,
                                        'index': user_profile.index,
                                        'city': user_profile.city,
                                        'street': user_profile.street,
                                        'house': user_profile.house,
                                      })
        else:
            form = Step3Form(request.POST)
            if form.is_valid():
                Order.get_or_create(request.user)
                return HttpResponseRedirect('/order/4/')
            
        c['form'] = form
        return render_to_response('order_3.html', c, context_instance=RequestContext(request))
    elif step == '4':
        if request.method == 'GET':
            return render_to_response('order_4.html', c, context_instance=RequestContext(request))
        else:
            o = Order.get_recent(request.user)
            if o:
                o.delivery = request.POST['delivery']
                o.save()
                return HttpResponseRedirect('/order/5/')
            else:
                return HttpResponseRedirect('/order/2/')
    elif step == '5':
        if request.method == 'GET':
            return render_to_response('order_5.html', c, context_instance=RequestContext(request))
        else:
            o = Order.get_recent(request.user)
            if o:
                o.send()
                c['order_send'] = True
                return render_to_response('order_5.html', c, context_instance=RequestContext(request))
            else:
                return HttpResponseRedirect('/order/2/')
    else:
        return HttpResponseRedirect('/cart/')
        

def contacts(request):
    reset_catalog(request)
    c = get_common_context(request)
    if request.method == 'GET':
        c['form'] = FeedbackForm()
    else:
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            form = FeedbackForm()
            c['msg_sent'] = u'Ваш отзыв отправлен. Спасибо.'
        else:
            c['request_form'] = form
        c['form'] = form
    return render_to_response('contacts.html', c, context_instance=RequestContext(request))

def opt(request):
    reset_catalog(request)
    c = get_common_context(request)
    if request.method == 'GET':
        c['form'] = RegisterOptForm()
    else:
        register_form = RegisterOptForm(request.POST)
        if register_form.is_valid():
            p1 = register_form.data.get('password_1')
            p2 = register_form.data.get('password_2')
            error = False
            if p1 != p2:
                register_form._errors["password_2"] = ErrorList([u'Пароли не совпадают.'])
                error = True
            if len(User.objects.filter(username=register_form.data.get('email'))):
                register_form._errors["email"] = ErrorList([u'Такой емейл уже зарегистрирован.'])
                error = True
            if not error:
                u = User(username=register_form.data.get('email'), email=register_form.data.get('email'))
                u.set_password(register_form.data.get('password_1'))
                u.save()
                p = u.get_profile()
                register_form = RegisterOptForm(request.POST, instance=p)
                register_form.save()
                p.send()
                user = auth.authenticate(username=register_form.data.get('email'), password=register_form.data.get('password_1'))
                auth.login(request, user)
                
                c['form'] = RegisterOptForm()
                c['msg_sent'] = u'Ваш отзыв отправлен. Спасибо.'
                return render_to_response('opt.html', c, context_instance=RequestContext(request))
            
        c['form'] = register_form
    return render_to_response('opt.html', c, context_instance=RequestContext(request))

def lk(request):
    c = get_common_context(request)
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'GET':
        c['form'] = ProfileForm(instance=request.user.get_profile())
    else:
        form = ProfileForm(request.POST, instance=request.user.get_profile())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/lk/')
        c['form'] = form
    return render_to_response('lk.html', c, context_instance=RequestContext(request))

def other_page(request, page_name):
    reset_catalog(request)
    c = get_common_context(request)
    try:
        c.update(Page.get_page_by_slug(page_name))
        return render_to_response('page.html', c, context_instance=RequestContext(request))
    except:
        raise Http404()

def register(request):
    c = get_common_context(request)
    
    auth_form = AuthenticationForm()
    register_form = RegisterForm()
    c['auth_form'] = auth_form
    c['register_form'] = register_form
    if request.method == "POST":
        if request.POST['action'] == 'auth':
            auth_form = AuthenticationForm(request.POST)
            if auth_form.is_valid():
                pass
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    if 'is_order' in request.session:
                        del request.session['is_order']
                        return HttpResponseRedirect('/order/2/')
                    return HttpResponseRedirect('/')
                else:
                    c['auth_error'] = u'Ваш аккаунт не активирован.'
                    
            else:
                c['auth_error'] = u'Неверный логин или пароль.'
            c['auth_form'] = auth_form
        elif request.POST['action'] == 'register':
            from django.forms.util import ErrorList
            
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                p1 = register_form.data.get('password_1')
                p2 = register_form.data.get('password_2')
                error = False
                if p1 != p2:
                    register_form._errors["password_2"] = ErrorList([u'Пароли не совпадают.'])
                    error = True
                if len(User.objects.filter(username=register_form.data.get('email'))):
                    register_form._errors["email"] = ErrorList([u'Такой емейл уже зарегистрирован.'])
                    error = True
                if not error:
                    u = User(username=register_form.data.get('email'), email=register_form.data.get('email'))
                    u.set_password(register_form.data.get('password_1'))
                    u.save()
                    p = u.get_profile()
                    p.fio = register_form.data.get('fio')
                    p.save()
                    user = auth.authenticate(username=register_form.data.get('email'), password=register_form.data.get('password_1'))
                    auth.login(request, user)
                    if 'is_order' in request.session:
                        del request.session['is_order']
                        return HttpResponseRedirect('/order/2/')
                    else:
                        return HttpResponseRedirect('/')
            c['register_form'] = register_form
                
    return render_to_response('register.html', c, context_instance=RequestContext(request))

def logout_user(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
