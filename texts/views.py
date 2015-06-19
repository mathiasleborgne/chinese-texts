#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from texts.models import Text
from django.views.generic import ListView, DetailView
from texts.forms import ContactForm


class TextList(ListView):
    model = Text
    context_object_name = "latest_texts"
    template_name = "texts/home.html"
    paginate_by = 5


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
