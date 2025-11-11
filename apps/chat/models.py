from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid

class Room(models.Model):
    ROOM_TYPES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES, default='public')
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_rooms')
    members = models.ManyToManyField(User, through='RoomMembership', related_name='joined_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + '-' + str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']

class RoomMembership(models.Model):
    ROLES = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('member', 'Member'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'room']
    
    def __str__(self):
        return f"{self.user.username} in {self.room.name}"

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
    
    class Meta:
        ordering = ['created_at']

class Attachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/%Y/%m/%d/')
    file_type = models.CharField(max_length=50)
    file_size = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Attachment for message {self.message.id}"  # type: ignore