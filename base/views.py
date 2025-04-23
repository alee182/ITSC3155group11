
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from .forms import UserProfileForm
from django.contrib.auth import logout

# Create your views here.
def home(request):
    return render(request,'base/home.html')

def explore(request):
    return render(request, 'base/explore.html')

def login_register(request):

    form = CreateUserForm()
    
    page = request.GET.get('page', 'login')
    
    context = {
        'page': page,
        'form': form
    }
    return render(request, 'base/login_register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('explore')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email:
            email = email.lower()
        else:
            messages.error(request, 'Please enter your email.')
            return redirect('login_register')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
            return redirect('login_register')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('explore')
        else:
            messages.error(request, 'Email OR password is incorrect')
            return redirect('login_register')

    return redirect('login_register')


def registerPage(request):
    """
    Handle register form submission
    """
    if request.user.is_authenticated:
        return redirect('explore')
        
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        email = request.POST.get('email').lower()
        if form.is_valid():
            
            if not email.endswith('@charlotte.edu'):
                messages.error(request, 'Email must end with "@charlotte.edu"')
                return redirect('auth')  # Change from login_register to auth
            
            # Save the user
            user = form.save(commit=False)
            user.email = email  # Set email field too
            user.save()
            
            # Log the user in
            login(request, user)
            return redirect('explore')
        else:
            # Form has errors - pass it back to the template
            # Map raw field names to friendly labels

# Display custom-labeled errors
            for errors in form.errors.values():
                for error in errors:
                    messages.error(request, error)


            return redirect('login_register') 

    # If not POST, redirect to the auth page with register parameter
    return redirect('login_register')  
def logoutUser(request):
    logout(request)
    return redirect('login_register') 

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
    return render(request, 'base/community.html')

