from django.shortcuts import render
from .models import *

def index(request):
    return render(request, 'index.html')

def contact(request):
    params = {
        'email': 'hotelcinco@estrelas.com',
        'contact': '+351 919293949'
    }
    return render(request, 'contact.html', params)

def about(request):
    return render(request, 'about.html')