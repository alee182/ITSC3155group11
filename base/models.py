from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Listing(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='static/images/listings', null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class DirectMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="recipient")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
