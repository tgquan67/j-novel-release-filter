from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def set_pref(request):

    return HttpResponse("setpref")


def index(request):

    return HttpResponse("okay")
