from django.contrib import admin
from .models import Report, ModerationAction

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['reported_by', 'message', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['reported_by__username', 'reason']

@admin.register(ModerationAction)
class ModerationActionAdmin(admin.ModelAdmin):
    list_display = ['moderator', 'target_user', 'action_type', 'created_at']
    list_filter = ['action_type', 'created_at']
    search_fields = ['moderator__username', 'target_user__username']