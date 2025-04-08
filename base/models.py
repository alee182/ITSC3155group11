from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Listing(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='static/images/listings', null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class DirectMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="recipient")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_pic = models.ImageField(upload_to='static/images/profile_pics', null=True, default='uncc-logo.png')

    USERNAME_FIELD = 'email'

class Report(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=255, choices=[('spam', 'Spam'), ('scam', 'Scam'), ('other', 'Other')])