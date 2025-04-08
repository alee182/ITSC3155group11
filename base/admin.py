from django.contrib import admin

# Register your models here.
from .models import Listing, DirectMessage, User, Report

admin.site.register(Listing)
admin.site.register(DirectMessage)
admin.site.register(User)
admin.site.register(Report)