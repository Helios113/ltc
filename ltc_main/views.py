from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    
    response = render(request, 'ltc/base.html')
    return response