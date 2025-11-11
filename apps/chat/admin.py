from django.contrib import admin
from .models import Room, RoomMembership, Message, Attachment

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'room_type', 'created_by', 'created_at']
    list_filter = ['room_type', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(RoomMembership)
class RoomMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'role', 'joined_at']
    list_filter = ['role', 'joined_at']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'room', 'content_preview', 'created_at', 'is_deleted']
    list_filter = ['is_deleted', 'created_at']
    search_fields = ['content', 'sender__username']
    
    def content_preview(self, obj):
        return obj.content[:50]

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['message', 'file_type', 'file_size', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at']