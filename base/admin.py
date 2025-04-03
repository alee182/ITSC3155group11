from django.contrib import admin

# Register your models here.
from .models import Listing, DirectMessage

admin.site.register(Listing)
admin.site.register(DirectMessage)