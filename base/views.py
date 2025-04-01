from django.shortcuts import render
# Create your views here.


from django.shortcuts import render
# Create your views here.
def homePage(request):
    return render(request, 'base/home.html')

def explorePage(request):
    return render(request, 'explore.html')

def communityPage(request):
    return render(request, 'community.html')

