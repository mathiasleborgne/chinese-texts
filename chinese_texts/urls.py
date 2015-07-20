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
from django.contrib.auth.views import password_change, password_change_done, \
    password_reset, password_reset_done, password_reset_confirm, \
    password_reset_complete, logout_then_login
from texts.views import TextList, ReadText, TextUpdate, TextCreate, \
    TextDelete, AuthorCreate, AuthorList, AuthorView


urlpatterns = patterns(
    'texts.views',
    url(r'^$', TextList.as_view(), name='texts_list'),
    url(r'^home$', TextList.as_view(), name='texts_list'),
    url(r'^text/(?P<pk>\d+)$', ReadText.as_view(), name='read_text'),
    url(r'^authors$', AuthorList.as_view(), name='authors'),
    url(r'^author/(?P<pk>\d+)$', AuthorView.as_view(), name='author_texts'),
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
    url(r'^about/$', 'about'),
    url(r'^search_texts/$', 'search_texts'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout_then_login$', logout_then_login, ),
    url(r'^password_change$', password_change,
        {'template_name': 'user_templates/password_change.html',
         'post_change_redirect': '/password_change_done'}),
    url(r'^password_change_done$', password_change_done,
        {'template_name': 'user_templates/password_change_done.html', }),
    url(r'^password_reset$', password_reset,
        {'template_name': 'user_templates/password_reset.html',
         'post_reset_redirect': '/password_reset_done'}),
    url(r'^password_reset_done$', password_reset_done,
        {'template_name': 'user_templates/password_reset_done.html', }),
    url(r'^password_reset_confirm$', password_reset_confirm,
        {'template_name': 'user_templates/password_reset_confirm.html', }),
    url(r'^password_reset_complete$', password_reset_complete,
        {'template_name': 'user_templates/password_reset_complete.html', }),

)
