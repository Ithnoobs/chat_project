import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import UserProfile

class PresenceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
            return
        
        self.user = self.scope["user"]
        self.presence_group = 'presence'
        
        # Join presence group
        await self.channel_layer.group_add(
            self.presence_group,
            self.channel_name
        )
        
        # Set user online
        await self.set_user_online(True)
        
        # Broadcast user online status
        await self.channel_layer.group_send(
            self.presence_group,
            {
                'type': 'user_status',
                'user_id': self.user.id,
                'username': self.user.username,
                'status': 'online'
            }
        )
        
        await self.accept()
    
    async def disconnect(self, code: int) -> None:
        if hasattr(self, 'user'):
            # Set user offline
            await self.set_user_online(False)
            
            # Broadcast user offline status
            await self.channel_layer.group_send(
                self.presence_group,
                {
                    'type': 'user_status',
                    'user_id': self.user.id,
                    'username': self.user.username,
                    'status': 'offline'
                }
            )
            
            # Leave presence group
            await self.channel_layer.group_discard(
                self.presence_group,
                self.channel_name
            )
    
    async def receive(self, text_data: str = None, bytes_data: bytes = None) -> None:
        if text_data:
            data = json.loads(text_data)
            # Handle heartbeat to keep connection alive
            if data.get('type') == 'heartbeat':
                await self.send(text_data=json.dumps({'type': 'heartbeat_ack'}))
    
    async def user_status(self, event: dict) -> None:
        # Send status update to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'status',
            'user_id': event['user_id'],
            'username': event['username'],
            'status': event['status']
        }))
    
    @database_sync_to_async
    def set_user_online(self, is_online: bool) -> None:
        profile = UserProfile.objects.get(user=self.user)
        profile.online_status = 'online' if is_online else 'offline'
        profile.save()