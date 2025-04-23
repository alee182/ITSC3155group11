from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Message, Listing


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'quantity', 'condition', 'created_by', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('condition', 'created_at')
    ordering = ('-created_at',)


admin.site.register(Message)
admin.site.register(User, UserAdmin)
