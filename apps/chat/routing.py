from django.urls import path
from apps.chat import consumers as chat_consumers
from apps.authentication import consumers as auth_consumers

websocket_urlpatterns = [
    path('ws/chat/<str:room_slug>/', chat_consumers.ChatConsumer.as_asgi()),
    path('ws/presence/', auth_consumers.PresenceConsumer.as_asgi()),
]