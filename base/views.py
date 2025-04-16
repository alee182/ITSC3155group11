from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
from .models import Post, Comment
from django.db.models import Q
from taggit.models import Tag
# Create your views here.

def home(request):
    return render(request, 'base/home.html')

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
