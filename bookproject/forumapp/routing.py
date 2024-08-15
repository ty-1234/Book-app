#routing.py specifies WebSocket URL patterns 
from django.urls import path
from . import consumers

#for HTTPS, use wss:// (WebSocket Secure) 
#instead of ws:// in your WebSocket URL
websocket_urlpatterns = [
    path('ws/forum/<int:thread_id>/', consumers.ChatConsumer.as_asgi()),
]
