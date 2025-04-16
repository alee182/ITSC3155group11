from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from base.models import User
from .models import Message

admin.site.register(Message)
admin.site.register(User, UserAdmin)