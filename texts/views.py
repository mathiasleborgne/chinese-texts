#-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, \
    render_to_response
from datetime import datetime
from texts.models import Text, Author, CharData
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from texts.forms import ContactForm, SearchTextsForm, TextForm, LoginForm, \
    AuthorForm, UserCreationMailForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.core.mail import mail_admins, send_mail
import json

template_prefix = "texts"


def make_template_name(suffix):
    return template_prefix + "/" + suffix + ".html"


class TextList(ListView):
    model = Text
    context_object_name = "latest_texts"
    template_name = make_template_name("home")
    paginate_by = 6


class ReadText(DetailView):
    context_object_name = "text"
    model = Text
    template_name = make_template_name("text")

    def get_context_data(self, **kwargs):
        context = super(ReadText, self).get_context_data(**kwargs)
        # decode metadata
        text = self.get_object()
        chars_data_json = text.chars_data
        json_decoder = json.decoder.JSONDecoder()
        if chars_data_json is not None:
            chars_data = [CharData.from_json(char_data_raw) for char_data_raw
                          in json_decoder.decode(chars_data_json)]
            context['chars_data_decoded'] = chars_data
        return context


class AuthorList(ListView):
    model = Author
    context_object_name = "authors"
    template_name = make_template_name("authors")


class AuthorView(DetailView):
    context_object_name = "author"
    model = Author
    template_name = make_template_name("author_page")

    def get_context_data(self, **kwargs):
        context = super(AuthorView, self).get_context_data(**kwargs)
        author = self.get_object()
        print author
        context['texts'] = Text.objects.filter(author=author)
        return context


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        successfully_sent = form.is_valid()
        subject = form.cleaned_data["subject"]
        message = "You had a message from steleforest/contact:\n" + \
            form.cleaned_data["message"]
        sender = form.cleaned_data["sender"]
        send_mail(subject, message, sender, ["mathias.leborgne@gmail.com"])
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


def author_page(request):
    # todo get the request author and filter
    texts = Text.objects.filter(author=author)[0]
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


class UserCreate(CreateView):
    model = User
    template_name = make_template_name("create_user")
    context_object_name = "user"
    form_class = UserCreationMailForm
    success_url = "/create_user_success"  # todo: "welcome, user!" page

def create_user_success(request):
    return render(request, make_template_name('create_user_success'), locals())


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
