import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Post, Thread

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['thread_id']
        self.room_group_name = f'chat_{self.room_name}'

        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope["user"]

        # Save the message to the database
        if user.is_authenticated:
            await self.save_post(self.room_name, message, user)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': user.username  # Send the username with the message
                }
            )

    # Ensure the chat_message event includes the username
    async def chat_message(self, event):
        message = event['message']
        username = event['username']  # Receive the username from the event
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @database_sync_to_async
    def save_post(self, thread_id, message, user):
        thread = Thread.objects.get(id=thread_id)
        post = Post.objects.create(
            thread=thread,
            message=message,
            created_by=user
        )
        post.save()