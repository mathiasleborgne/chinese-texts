#-*- coding: utf-8 -*-

"""chinese_texts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from texts.views import TextList, ReadText, TextUpdate, TextCreate, \
    TextDelete, AuthorCreate


urlpatterns = patterns(
    'texts.views',
    url(r'^home$', TextList.as_view(), name='texts_list'),
    url(r'^text/(?P<pk>\d+)$', ReadText.as_view(), name='read_text'),
    url(r'^contact/$', 'contact'),
    url(r'^log_in/$', 'log_in'),
    url(r'^log_out/$', 'log_out'),
    url(r'^new_text/$', TextCreate.as_view(), name='new_text'),
    url(r'^create_author/$', AuthorCreate.as_view(), name='create_author'),
    url(r'^update_text/(?P<pk>\d+)$', TextUpdate.as_view(),
        name='update_text'),
    url(r'^update_text/update_success$', 'update_success'),
    url(r'^delete_text/(?P<pk>\d+)$', TextDelete.as_view(),
        name='delete_text'),
    url(r'^search_texts/$', 'search_texts'),
    url(r'^admin/', include(admin.site.urls)),
)
