import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from message.models import Message
from authentication.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            # Close the connection if the user is not authenticated
            await self.close()
        else:
            self.room_name = 'public_room'
            self.room_group_name = self.room_name

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name, self.channel_name
            )
            await self.accept()

    async def disconnect(self, code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        json_text = json.loads(text_data)
        message = json_text["message"]
        receiver = json_text["receiver"]

        await self.save_message(message, receiver)
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, 
            {
                "type": "chat_message", 
                "message": message
            }
        )
    
    @database_sync_to_async
    def save_message(self, message, receiver):
        receiver = User.objects.get(first_name = "Robert", last_name = "Wald")
        Message.objects.create(content=message, sender=self.scope["user"], receiver=receiver)

    async def chat_message(self, event):
        message = event['message']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
