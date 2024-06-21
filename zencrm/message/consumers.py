import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message
from authentication.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender = self.scope['url_route']['kwargs']['sender']
        self.receiver = self.scope['url_route']['kwargs']['receiver']
        self.room_group_name = f'chat_{self.sender}_{self.receiver}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Fetch and send initial messages
        messages = await self.get_messages()
        await self.send(text_data=json.dumps({
            'type': 'initial_messages',
            'messages': messages
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Save message to database
        await self.save_message(self.sender, self.receiver, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.sender,
                'receiver': self.receiver,
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'sender': event['sender'],
            'receiver': event['receiver'],
        }))

    @sync_to_async
    def get_messages(self):
        messages = Message.objects.filter(sender=self.sender, receiver=self.receiver).order_by('timestamp') | Message.objects.filter(sender=self.receiver, receiver=self.sender).order_by('timestamp')
        return [{'sender': msg.sender.username, 'receiver': msg.receiver.username, 'message': msg.message, 'timestamp': msg.timestamp.strftime("%I:%M %p  %d-%b-%y")} for msg in messages]

    @sync_to_async
    def save_message(self, sender, receiver, message):
        sender = User.objects.get(pk = sender)
        receiver = User.objects.get(pk = receiver)
        Message.objects.create(sender=sender, receiver=receiver, message=message)
