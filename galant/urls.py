# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

import settings
import views

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
    url(r'^settings/', include('livesettings.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^accounts/', include('registration.urls')),

    url(r'^$' , views.home_page),
    url(r'^category/(?P<slug>[\w-]+)/$', views.category),
    url(r'^category/$', views.category, {'slug': None}),
    url(r'^item/(?P<slug>[\w-]+)/$' , views.item),
    
    url(r'^news/(?P<slug>[\w-]+)/$' , views.news),
    url(r'^news/$' , views.news),
    
    #url(r'^request$' , views.request_page),
    
    #url(r'^category/(?P<category_id>\w+)$' , views.category_page),
    
    
    url(r'^(?P<page_name>[\w-]+)/$' , views.other_page),
    
)
