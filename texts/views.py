#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from texts.models import Text
from django.views.generic import ListView, DetailView
from texts.forms import ContactForm, SearchTextsForm


class TextList(ListView):
    model = Text
    context_object_name = "latest_texts"
    template_name = "texts/home.html"
    paginate_by = 10


class ReadText(DetailView):
    context_object_name = "text"
    model = Text
    template_name = "texts/text.html"


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        successfully_sent = form.is_valid()
    else:
        form = ContactForm()
    return render(request, 'texts/contact.html', locals())


def search_texts(request):
    was_valid_search = False
    if request.method == 'POST':
        form = SearchTextsForm(request.POST)
        if form.is_valid():
            was_valid_search = True
            keyword = form.cleaned_data["keyword"]
            print keyword
            searched_texts = Text.search_texts(keyword)
    else:
        form = SearchTextsForm()
    return render(request, 'texts/search_texts.html', locals())
