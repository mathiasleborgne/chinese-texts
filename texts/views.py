#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from texts.models import Text
from django.views.generic import ListView, DetailView
from texts.forms import ContactForm, SearchTextsForm, TextForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse


template_prefix = "texts"


def make_template_name(suffix):
    return template_prefix + "/" + suffix + ".html"


class TextList(ListView):
    model = Text
    context_object_name = "latest_texts"
    template_name = make_template_name("home")
    paginate_by = 10


class ReadText(DetailView):
    context_object_name = "text"
    model = Text
    template_name = make_template_name("text")


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        successfully_sent = form.is_valid()
    else:
        form = ContactForm()
    return render(request, make_template_name("contact"), locals())


def update_success(request):
    return render(request, "texts/update_text/update_success", locals())


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
    return render(request, make_template_name("search_texts"), locals())


class TextUpdate(UpdateView):
    model = Text
    template_name = make_template_name("update_text")
    context_object_name = "text"
    form_class = TextForm
    success_url = "/home"
    is_update = True
    # todo success_url: print article

    # def get_success_url(self):
    #     return reverse('read_text', kwargs={'pk': self._id})


class TextCreate(CreateView):
    model = Text
    template_name = make_template_name("create_text")
    context_object_name = "text"
    form_class = TextForm
    success_url = "/home"
    is_update = False
    # todo success_url: print article


class TextDelete(DeleteView):
    model = Text
    template_name = make_template_name("delete_text")
    context_object_name = "text"
    success_url = "/home"
