import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class NotificationConsumer(WebsocketConsumer):
   def connect(self):
    self.accept()
    self.user_id = self.scope["user"].id  # Assuming you have set up authentication
    self.group_name = f'user_{self.user_id}'
    async_to_sync(self.channel_layer.group_add)(
        self.group_name,
        self.channel_name
    )

def disconnect(self, close_code):
    async_to_sync(self.channel_layer.group_discard)(
        self.group_name,
        self.channel_name
    )
    
    
def receive(self, text_data):
        pass  # No need to process incoming messages from clients

def notification_message(self, event):
        notification_data = event['message']
        self.send(text_data=json.dumps(notification_data))

def send_reading_reminder(self, group_name, message):
     self.channel_layer.group_send(
        group_name,
        {
            'type': 'notification_message',
            'message': message
        }
    )
