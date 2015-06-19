#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime


def home(request):
    return render(request, 'texts/home.html')


def text(request, text_id):
    return render(request, 'texts/text.html', locals())
