from django.db import models
from django.contrib.auth.models import User
from apps.chat.models import Message

class Report(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ]
    
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='reports')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Report by {self.reported_by.username} - {self.status}"

class ModerationAction(models.Model):
    ACTION_TYPES = [
        ('ban', 'Ban User'),
        ('mute', 'Mute User'),
        ('delete', 'Delete Message'),
        ('warn', 'Warn User'),
    ]
    
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moderation_actions')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_actions')
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    reason = models.TextField()
    duration = models.IntegerField(null=True, blank=True, help_text="Duration in minutes for temporary actions")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.action_type} - {self.target_user.username} by {self.moderator.username}"