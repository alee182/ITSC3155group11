from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def explore(request):
    return render(request, 'explore.html')

def listing(request):
    return render(request, 'sales.html')


def messaging(request):
    return render(request, 'message.html')
