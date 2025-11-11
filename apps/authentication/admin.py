from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'online_status', 'last_seen', 'created_at']
    list_filter = ['online_status', 'created_at']
    search_fields = ['user__username', 'user__email']