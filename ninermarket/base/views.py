from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return HttpResponse('Home page')

def explore(request):
    return HttpResponse('Explore Page')

def listing(request):
    return HttpResponse('LISTING')


def messaging(request):
    return HttpResponse("MESSAGE")

