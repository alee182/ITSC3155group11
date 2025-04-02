from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
# Create your views here.
def homePage(request):
    return render(request, 'base/home.html')

def explorePage(request):
    return render(request, 'explore.html')

def communityPage(request):
    return render(request, 'community.html')

