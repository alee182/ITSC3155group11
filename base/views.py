
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm
from .forms import UserProfileForm

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

            username = form.cleaned_data.get('username')
            if not username.lower().endswith('@charlotte.edu'):
                messages.error(request, 'Username must end with "@charlotte.edu"')
            else:
                user = form.save(commit=False)
                user.username = username.lower()
                user.save()
                login(request, user)
                return redirect('explore')



    return  render(request, 'ninermarket/templates/login_register.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})

def listing(request):
    return render(request, 'sales.html')

@login_required(login_url='login')
def messaging(request):
    return render(request, 'message.html')


def community(request):
    return render(request, 'community.html')

