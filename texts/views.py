#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from texts.models import Text


def home(request):
    return render(request, 'texts/home.html',
                  {'latest_texts': Text.objects.all()})


def read(request, text_id):
    text = get_object_or_404(Text, id=text_id)
    return render(request, 'texts/text.html', {'text': text})
