from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Listing(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    