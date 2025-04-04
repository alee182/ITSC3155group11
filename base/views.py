from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def explore(request):
    return render(request, 'explore.html')

def community(request):
    return render(request, 'community.html')
