from django.shortcuts import render, get_object_or_404, redirect
from .models import Thread, Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def messages_view(request, thread_id=None):
    threads = Thread.objects.filter(participants=request.user)

    selected_thread = None
    messages = []

    if thread_id:
        selected_thread = get_object_or_404(Thread, id=thread_id)
        if request.user not in selected_thread.participants.all():
            return redirect('messages')  # security: user not in this thread
        messages = selected_thread.messages.all()

    if request.method == "POST" and selected_thread:
        content = request.POST.get("content")
        if content:
            Message.objects.create(thread=selected_thread, sender=request.user, content=content)
            return redirect('messages_view', thread_id=thread_id)

    return render(request, "messages.html", {
        "threads": threads,
        "selected_thread": selected_thread,
        "messages": messages
    })
