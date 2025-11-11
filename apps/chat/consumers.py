import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Room, Message
from typing import Any

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self) -> None:
        self.room_slug = self.scope.get('url_route', {}).get('kwargs', {}).get('room_slug', '')
        self.room_group_name = f'chat_{self.room_slug}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, code: int) -> None:
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data: str = None, bytes_data: bytes = None) -> None:
        if text_data:
            data = json.loads(text_data)
            message_type = data.get('type', 'message')
            
            if message_type == 'message':
                message = data['message']
                username = data['username']
                
                # Save message to database
                await self.save_message(username, message)
                
                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'username': username,
                    }
                )
            elif message_type == 'typing':
                # Broadcast typing indicator
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'typing_indicator',
                        'username': data['username'],
                        'is_typing': data['is_typing'],
                    }
                )
    
    async def chat_message(self, event: dict) -> None:
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'username': event['username'],
        }))
    
    async def typing_indicator(self, event: dict) -> None:
        # Send typing indicator to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'username': event['username'],
            'is_typing': event['is_typing'],
        }))
    
    @database_sync_to_async
    def save_message(self, username: str, message: str) -> None:
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=self.room_slug)
        Message.objects.create(
            room=room,
            sender=user,
            content=message
        )