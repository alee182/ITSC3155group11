
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def home(request):
    return render(request,'home.html')

def explore(request):
    return render(request, 'explore.html')

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('explore')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try: 
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('explore')
        else:
            messages.error(request, 'Username OR password does not exist')


    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('explore')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('explore')
        else: 
            messages.error(request, 'An error occured during registration')


    return  render(request, 'base/login_register.html', {'form': form})




def listing(request):
    return render(request, 'sales.html')

@login_required(login_url='login')
def messaging(request):
    return render(request, 'message.html')


def community(request):
    return render(request, 'community.html')

