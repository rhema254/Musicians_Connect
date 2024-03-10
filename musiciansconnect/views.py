from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.contrib import messages


# Create your views here.

def basehtmltrial(request):
    return render(request, "base.html")
