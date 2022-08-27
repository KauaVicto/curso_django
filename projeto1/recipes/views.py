from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return HttpResponse('<h1>HOME 1</h1>')


def sobre(request):
    return HttpResponse('SOBRE 1')


def contato(request):
    return HttpResponse('CONTATO 1')
