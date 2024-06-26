import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from .models import Message, Conversation
from authentication.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender = self.scope['url_route']['kwargs']['sender']        
        self.receiver = self.scope['url_route']['kwargs']['receiver']        

        self.group_name = f"chat_{min(self.sender, self.receiver)}_{max(self.sender, self.receiver)}"

        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        await self.send_initial_data()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Save message to database
        message = await self.save_message(self.sender, self.receiver, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message.message,
            'sender': message.sender.username,
            'receiver': message.receiver.username,
            'timestamp': message.timestamp.strftime("%I:%M %p %d-%b-%y")
        }))
    

    @sync_to_async
    def save_message(self, sender, receiver, message):
        self.sender = sender
        self.receiver = receiver
        sender = User.objects.get(pk = self.sender)
        receiver = User.objects.get(pk = self.receiver)
        participants = sorted([sender, receiver], key=lambda x: x.pk)
        conversation = Conversation.objects.filter(participants = participants[0]).filter(participants = participants[1]).first()
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.set(participants)
            conversation.save()

        message = Message.objects.create(conversation = conversation, sender=sender, receiver=receiver, message=message)
        return message

    async def send_initial_data(self):
        conversation = await self.get_conversation()
        if conversation:
            await self.send(text_data = json.dumps({
                'type': 'initial_data',
                'conversation_id': conversation.pk,
                'participant_1': list(conversation.participants.all())[0].full_name,
                'participant_2': list(conversation.participants.all())[1].full_name,         
            }))


    @sync_to_async
    def get_conversation(self):
        self.sender = self.scope['user'].pk
        self.receiver = self.scope['url_route']['kwargs']['receiver']
        self.sender_obj = User.objects.get(pk = self.sender)
        self.receiver_obj = User.objects.get(pk = self.receiver)

        conversation = Conversation.objects.filter(participants = self.sender).filter(participants = self.receiver).first()

        if not conversation:
            participants = sorted([self.sender_obj, self.receiver_obj], key=lambda x: x.pk)

            conversation = Conversation.objects.create()
            conversation.participants.set(participants)
            conversation.save()

            return conversation
        
        return None




class ConversationChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['conversation_id']

        await self.accept()

        await self.send_initial_data(self.group_name)



    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass

    @sync_to_async
    def get_messages(self, conversation):
        messages = Message.objects.filter(conversation=self.group_name).order_by('timestamp')
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
    
    async def send_initial_data(self):
        messages = await self.get_messages(self.group_name)
        await self.send(text_data=json.dumps({
            'type': 'initial_messages',
            'messages': messages
        }))