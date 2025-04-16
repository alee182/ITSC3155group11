from django.contrib import admin
from .models import Message
from .models import Listing, DirectMessage, User, Report
admin.site.register(Message)
admin.site.register(Listing)
admin.site.register(DirectMessage)
admin.site.register(User)
admin.site.register(Report)
