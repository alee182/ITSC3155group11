
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserCreationForm

listings = [
    {'id':1, 'name': 'Textbook', 'price': 20, 'image': '/static/listing-images/textbook.jpeg'},
    {'id':2, 'name': 'Lava Lamp', 'price': 15, 'image': '/static/listing-images/lavalamp.jpg'},
    {'id':3, 'name': 'Doorway Carpet', 'price': 10, 'image': '/static/listing-images/doorcarpet.jpeg'},
    {'id':4, 'name': 'Calculator', 'price': 10, 'image': '/static/listing-images/calculator.jpeg'},
    {'id':5, 'name': 'Shirt Hangers', 'price': 6, 'image': '/static/listing-images/shirthangers.jpeg'},
]

# Create your views here.
def home(request):
    return render(request, 'home.html')

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

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
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')


    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else: 
            messages.error(request, 'An error occured during registration')


    return  render(request, 'base/login_register.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def explore(request):
    #search-bar functionality
    query = request.GET.get('q', '')
    if query:
        filtered = [l for l in listings if query.lower() in l['name'].lower()]
    else:
        filtered = listings
    return render(request, 'explore.html', {'listings': filtered, 'query': query})

def listing(request, pk):
    listing = None
    for i in listings:
        if i['id'] == int(pk):
            listing = i
            break
    return render(request, 'listing.html', {'listing':i})

@login_required(login_url='login')
def messaging(request):
    return render(request, 'message.html')

def community(request):
    return render(request, 'community.html')
