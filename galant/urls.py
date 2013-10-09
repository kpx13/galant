# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

import settings
import views

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^accounts/', include('registration.urls')),

    url(r'^$' , views.home_page),
    
    #url(r'^request$' , views.request_page),
    #url(r'^item/(?P<item_id>\w+)$' , views.item_page),
    #url(r'^category/(?P<category_id>\w+)$' , views.category_page),
    
    
    url(r'^(?P<page_name>\w+)$' , views.other_page),
    
)
