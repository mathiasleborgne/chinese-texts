#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from texts.models import Text, Author
from django.views.generic import ListView, DetailView
from texts.forms import ContactForm, SearchTextsForm, TextForm, LoginForm, \
    AuthorForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout


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


class AuthorCreate(CreateView):
    model = Author
    template_name = make_template_name("create_author")
    context_object_name = "author"
    form_class = AuthorForm
    success_url = "/home"


def log_in(request):
    # todo use generic view
    error = False
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                error = True
    else:
        form = LoginForm()
    return render(request, make_template_name("log_in"), locals())


def log_out(request):
    # todo use generic view
    logout(request)
    return redirect(reverse(log_in))


def about(request):
    texts_count = Text.count_texts()
    return render(request, make_template_name("about"), locals())
