from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message, Post, Comment, Listing, ListingImage
from django.contrib import messages
from base.models import User
from django.db.models import Q
from taggit.models import Tag
from django.contrib.auth import authenticate, login, logout
from .forms import ListingForm, UserProfileForm, CreateUserForm
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()
# Create your views here.

def home(request):
    return render(request, 'base/index.html')

@login_required
def message_view(request, username=None):
    users = User.objects.exclude(username=request.user.username)
    selected_user = User.objects.get(username=username) if username else None

    messages = []
    if selected_user:
        messages = Message.objects.filter(
    sender__in=[request.user, selected_user],
    receiver__in=[request.user, selected_user]
    ).order_by("timestamp")

    if request.method == "POST":
        content = request.POST.get("message")
        if selected_user and content:
            Message.objects.create(sender=request.user, receiver=selected_user, content=content)
            return redirect('message', username=selected_user.username)

    return render(request, "base/message.html", {
        "users": users,
        "selected_user": selected_user,
        "messages": messages
    })

@login_required(login_url=settings.LOGIN_URL)
def community_view(request):
    tag = request.GET.get('tag')
    search_query = request.GET.get('q', '')

    if tag:
        posts = Post.objects.filter(tags__name__icontains=tag).distinct().order_by('-start_date')
    elif search_query:
        posts = Post.objects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct().order_by('-start_date')
    else:
        posts = Post.objects.all().order_by('-start_date')

    return render(request, 'base/community.html', {
        'posts': posts,
        'selected_tag': tag,
        'search_query': search_query,
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        image = request.FILES.get('image')
        tag_input = request.POST.get('tags', '')

        post = Post.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            image=image,
            created_by=request.user
        )

        # Add tags (comma-separated string into Taggit)
        if tag_input:
            tags = [tag.strip() for tag in tag_input.split(',') if tag.strip()]
            post.tags.add(*tags)

        return redirect('community')

    # Pass all existing tags to the template for dropdown
    all_tags = Tag.objects.all()
    return render(request, 'base/create_post.html', {'all_tags': all_tags})



def explore(request):
    return render(request, 'base/explore.html')


def community_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).order_by('created_at')

    if request.method == 'POST':
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            body=request.POST.get('body')
        )
        return redirect('community-detail', post_id=post.id)

    context = {
        'post': post,
        'comments': comments
    }
    return render(request, 'base/community_detail.html', context)

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user == post.created_by:
        post.delete()
        return redirect('community')
    return redirect('community-detail', post_id=pk)

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
def sales_page(request):
    query = request.GET.get('q', '')
    listings = Listing.objects.filter(created_by=request.user)

    if query:
        listings = listings.filter(title__icontains=query)

    return render(request, 'base/sales.html', {
        'listings': listings,
        'query': query
    })

@login_required
def create_sale(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        images = request.FILES.getlist('images')  # Get all uploaded files

        if form.is_valid():
            listing = form.save(commit=False)
            listing.created_by = request.user
            listing.accepted_payments = ','.join(form.cleaned_data['accepted_payments'])
            listing.save()

            # Save each uploaded image
            for img in images:
                ListingImage.objects.create(listing=listing, image=img)

            return redirect('sales')
    else:
        form = ListingForm()
    
    return render(request, 'base/create_sale.html', {'form': form})

@login_required
def edit_sale(request, pk):
    listing = get_object_or_404(Listing, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)

        if form.is_valid():
            form.save()

            # Handle new image uploads
            files = request.FILES.getlist('images')
            for f in files:
                ListingImage.objects.create(listing=listing, image=f)

            messages.success(request, 'Listing updated successfully!')
            return redirect('sales')
    else:
        form = ListingForm(instance=listing)

    return render(request, 'base/edit_sale.html', {'form': form, 'listing': listing})

@login_required
def delete_sale(request, pk):
    listing = get_object_or_404(Listing, pk=pk, created_by=request.user)
    if request.method == 'POST':
        listing.delete()
        return redirect('sales')
    return redirect('edit_sale', pk=pk)

def explore(request):
    listings = Listing.objects.all()
    query = request.GET.get('q')
    if query:
        listings = listings.filter(title__icontains=query)
    return render(request, 'base/explore.html', {'listings': listings, 'query': query})


def explore_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'base/explore_detail.html', {'listing': listing})