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
    TextDelete, AuthorCreate, AuthorUpdate, AuthorList, AuthorView, UserCreate


urlpatterns = patterns(
    'texts.views',
    url(r'^$', 'highlighted_texts', name="highlighted_texts"),
    url(r'^texts-list$', TextList.as_view(), name='texts_list'),
    url(r'^text/(?P<pk>\d+)$', ReadText.as_view(), name='read_text'),
    url(r'^authors$', AuthorList.as_view(), name='authors'),
    url(r'^author-page/(?P<pk>\d+)$', AuthorView.as_view(), name='author_page'),
    url(r'^contact/$', 'contact', name="contact"),
    url(r'^create-user/$', UserCreate.as_view(), name='create_user'),
    url(r'^create-user-success/$', 'create_user_success', name='create_user_success'),
    url(r'^log-in/$', 'log_in', name="log_in"),
    url(r'^log-out/$', 'log_out', name="log_out"),
    url(r'^create-author/$', AuthorCreate.as_view(), name='create_author'),
    url(r'^update-author/(?P<pk>\d+)$', AuthorUpdate.as_view(),
        name='update_author'),
    url(r'^new-text/$', TextCreate.as_view(), name='new_text'),
    url(r'^update-text/(?P<pk>\d+)$', TextUpdate.as_view(),
        name='update_text'),
    url(r'^update-text/update-success$', 'update_success',
            name="update_text_success"),
    url(r'^delete-text/(?P<pk>\d+)$', TextDelete.as_view(),
        name='delete_text'),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^about/$', 'about', name="about"),
    url(r'^poll/$', 'poll', name="poll"),
    url(r'^search-texts/$', 'search_texts', name="search_texts"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout-then-login$', logout_then_login, name="logout_then_login"),
    # password reset
    url(r'^user/password/reset/$', password_reset,
        {'template_name': 'registration/password_reset.html',
         'email_template_name': 'registration/password_reset_email.html',
         'post_reset_redirect' : '/user/password/reset/done/'},
         name="password_reset"),
    url(r'^user/password/reset/done/$', password_reset_done,
        {'template_name': 'registration/password_reset_done.html'}),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$',
        password_reset_confirm,
        {'template_name': 'registration/password_reset_confirm.html',
         'post_reset_redirect' : '/user/password/done/'},
        name='password_reset_confirm'),
    url(r'^user/password/done/$', password_reset_complete,
        {'template_name': 'registration/password_reset_complete.html', }),
)
