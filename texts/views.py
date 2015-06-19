#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime


def home(request):
    """ Exemple de page HTML, non valide pour que l'exemple soit concis """
    text = u"""<h1>Bienvenue sur mon blog !</h1>
               <p>Les crêpes bretonnes ça tue des mouettes en plein vol !</p>"""
    return HttpResponse(text)


def date_actuelle(request):
    return render(request, 'texts/date.html', {'date': datetime.now()})


def poem(request, nombre1, nombre2):
    total = int(nombre1) + int(nombre2)

    # Retourne nombre1, nombre2 et la somme des deux au tpl
    return render(request, 'texts/poem.html', locals())
