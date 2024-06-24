import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from .models import Message, Conversation
from authentication.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender = self.scope['url_route']['kwargs']['sender']
        print(self.sender)
        self.receiver = self.scope['url_route']['kwargs']['receiver']
        print(self.receiver)
        self.room_group_name = f'chat_{self.sender}_{self.receiver}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # # Fetch and send initial messages
        # messages = await self.get_messages()
        # await self.send(text_data=json.dumps({
        #     'type': 'initial_messages',
        #     'messages': messages
        # }))

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
    
    @database_sync_to_async
    def get_conversations(self):
        conversations = Conversation.objects.all()
        print(conversations)
        return [{'conversation_id': conversation.pk} for conversation in conversations]

    @sync_to_async
    def save_message(self, sender, receiver, message):
        sender = User.objects.get(pk = sender)
        receiver = User.objects.get(pk = receiver)
        participants = sorted([sender, receiver], key=lambda x: x.pk)
        conversation = Conversation.objects.filter(participants = participants[0]).filter(participants = participants[1]).first()
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.set(participants)
        Message.objects.create(conversation = conversation, sender=sender, receiver=receiver, message=message)


    async def send_initial_data(self):
        messages = await self.get_messages()
        print(messages)
        await self.send(text_data=json.dumps({
            'type': 'initial_messages',
            'messages': messages
        }))

        conversations = await self.get_conversations()
        print(conversations)
        await self.send(text_data=json.dumps({
            'type': 'initial_messages',
            'conversations': conversations
        }))


class ConversationChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.conversation = self.scope['url_route']['kwargs']['conversation_id']

        await self.accept()

        await self.send_initial_data(self.conversation)



    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass

    @sync_to_async
    def get_messages(self, conversation):
        messages = Message.objects.filter(conversation=self.conversation).order_by('timestamp')
        return [{
            'sender': msg.sender.username,
            'sender_id' : msg.sender.pk,
            'sender_image': msg.sender.image.url if msg.sender.image else None,
            'sender_full_name' : msg.sender.full_name if msg.sender.full_name else None,

            'receiver': msg.receiver.username,
            'receiver_id' : msg.receiver.pk,
            'receiver_full_name' : msg.receiver.full_name if msg.receiver.full_name else None,

            'message': msg.message,
            'timestamp': msg.timestamp.strftime("%I:%M %p %d-%b-%y")
        } for msg in messages]
    
    async def send_initial_data(self, conversation):
        messages = await self.get_messages(self.conversation)
        await self.send(text_data=json.dumps({
            'type': 'initial_messages',
            'messages': messages
        }))