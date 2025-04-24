from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message, Post, Comment, Listing, ListingImage, Review
from django.contrib import messages
from base.models import User
from django.db.models import Q
from taggit.models import Tag
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import UserProfileForm, ListingForm, ReviewForm
from django.contrib.auth import get_user_model
from django.utils.text import slugify
# Create your views here.

def home(request):
    return render(request, 'base/index.html')

User = get_user_model()

@login_required
def message_view(request, slug=None):
    users = User.objects.exclude(id=request.user.id)
    selected_user = None
    messages_qs = []

    if slug:
        for user in users:
            if slugify(f"{user.first_name} {user.last_name}") == slug:
                selected_user = user
                break

    if selected_user:
        messages_qs = Message.objects.filter(
            sender__in=[request.user, selected_user],
            receiver__in=[request.user, selected_user]
        ).order_by("timestamp")

    if request.method == "POST":
        content = request.POST.get("message")
        if selected_user and content:
            Message.objects.create(
                sender=request.user,
                receiver=selected_user,
                content=content
            )
            return redirect('message', slug=selected_user.full_name_slug)

    return render(request, "base/message.html", {
        "users": users,
        "selected_user": selected_user,
        "messages": messages_qs
    })



@login_required
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



def explore_view(request):
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

@login_required
def edit_profile_pic(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        if profile_pic:
            request.user.profile_pic = profile_pic
            request.user.save()
    return redirect('profile')

@login_required
def edit_first_name(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        if first_name:
            request.user.first_name = first_name
            request.user.save()
            return redirect('profile')
    return render(request, 'base/edit_first_name.html')

@login_required
def edit_last_name(request):
    if request.method == 'POST':
        last_name = request.POST.get('last_name')
        if last_name:
            request.user.last_name = last_name
            request.user.save()
            return redirect('profile')
    return render(request, 'base/edit_last_name.html')

@login_required
def edit_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            request.user.email = email
            request.user.save()
            return redirect('profile')
    return render(request, 'base/edit_email.html')

def listing(request):
    return render(request, 'sales.html')

@login_required
def profile(request):
    return render(request, 'base/userprofile.html')

def login_register(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'login':
            username = request.POST.get('username').lower()
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('explore')
            else:
                messages.error(request, 'Invalid login credentials.')

        elif form_type == 'signup':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username').lower()
                if not username.endswith('@charlotte.edu'):
                    messages.error(request, 'Email must end with "@charlotte.edu".')
                else:
                    user = form.save(commit=False)
                    user.username = username
                    user.save()
                    login(request, user)
                    return redirect('explore')
            else:
                messages.error(request, 'Signup failed. Check your form and try again.')

    else:
        form = UserCreationForm()

    return render(request, 'base/login_register.html')

@login_required
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

@login_required
def explore_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    reviews = listing.reviews.all().order_by('-created_at')

    # Handle review submission
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.listing = listing
            review.save()
            return redirect('explore_detail', pk=pk)
    else:
        form = ReviewForm()

    return render(request, 'base/explore_detail.html', {
        'listing': listing,
        'form': form,
        'reviews': reviews
    })
