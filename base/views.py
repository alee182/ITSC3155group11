from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User
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
    return render(request, 'base/community.html')  # Update path if needed

@login_required
def create_post(request):
    return render(request, 'base/create_post.html')
