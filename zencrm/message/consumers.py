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

        await self.accept()

        self.conversation, just_created = await self.get_conversation()

        if just_created == True:
            print("populating")
            await self.send_conversation_data()

    async def receive(self):
        message = self.scope['message']

        get_message = await self.save_message()

    async def disconnect(self, close_code):
        pass

    @sync_to_async
    def get_conversation(self):
        self.sender_obj = User.objects.get(pk = self.sender)
        self.receiver_obj = User.objects.get(pk = self.receiver)
        
        conversation = Conversation.objects.filter(participants=self.sender_obj).filter(participants=self.receiver_obj).first()

        just_created = False

        if not conversation:
            participants = sorted([self.sender_obj, self.receiver_obj], key=lambda x: x.pk)

            conversation = Conversation.objects.create()
            conversation.participants.set(participants)
            conversation.save()

            just_created = True

        return conversation, just_created
    
    @sync_to_async
    def save_message(self):
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

    
    async def send_conversation_data(self):
        await self.send(text_data = json.dumps({
                'type': 'conversation_data',
                'conversation_id': self.conversation.pk,
                'conversation_image': self.receiver_obj.image.url if self.receiver_obj.image else None,
                'conversation_name': self.receiver_obj.full_name,                
            }))

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.sender = self.scope['url_route']['kwargs']['sender']        
#         self.receiver = self.scope['url_route']['kwargs']['receiver']        

#         self.group_name = f"chat_{min(self.sender, self.receiver)}_{max(self.sender, self.receiver)}"

#         # Join room group
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )

#         await self.accept()

#         await self.send_initial_data()


#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data['message']

#         # Save message to database
#         message = await self.save_message(self.sender, self.receiver, message)

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#             }
#         )

#     async def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'type': 'chat_message',
#             'message': message.message,
#             'sender': message.sender.username,
#             'receiver': message.receiver.username,
#             'timestamp': message.timestamp.strftime("%I:%M %p %d-%b-%y")
#         }))
    

#     @sync_to_async
#     def save_message(self, sender, receiver, message):
#         self.sender = sender
#         self.receiver = receiver
#         sender = User.objects.get(pk = self.sender)
#         receiver = User.objects.get(pk = self.receiver)
#         participants = sorted([sender, receiver], key=lambda x: x.pk)
#         conversation = Conversation.objects.filter(participants = participants[0]).filter(participants = participants[1]).first()
#         if not conversation:
#             conversation = Conversation.objects.create()
#             conversation.participants.set(participants)
#             conversation.save()

#         message = Message.objects.create(conversation = conversation, sender=sender, receiver=receiver, message=message)
#         return message

#     async def send_initial_data(self):
#         conversation_detail = await self.get_conversation()
#         if conversation_detail:
#             await self.send(text_data = json.dumps({
#                 'type': 'initial_data',
#                 'conversation_id': conversation_detail['conversation_id'],
#                 'conversation_image': conversation_detail['conversation_image'],
#                 'conversation_name': conversation_detail['conversation_name'],
#                 'participant_1': conversation_detail['participants'][0].full_name,
#                 'participant_2': conversation_detail['participants'][1].full_name,         
#             }))


#     @sync_to_async
#     def get_conversation(self):
#         self.sender = self.scope['user'].pk
#         self.receiver = self.scope['url_route']['kwargs']['receiver']
#         self.sender_obj = User.objects.get(pk = self.sender)
#         self.receiver_obj = User.objects.get(pk = self.receiver)

#         conversation = Conversation.objects.filter(participants = self.sender).filter(participants = self.receiver).first()

#         if not conversation:
#             participants = sorted([self.sender_obj, self.receiver_obj], key=lambda x: x.pk)

#             conversation = Conversation.objects.create()
#             conversation.participants.set(participants)
#             conversation.save()

#             conversation_image = self.receiver_obj.image.url if self.receiver_obj.image else None
#             conversation_name = self.receiver_obj.full_name

#             return {'conversation_id': conversation.pk, 'conversation_name': conversation_name, 'participants': participants, 'conversation_image': conversation_image}
        
#         return None




# class ConversationChatConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         self.group_name = self.scope['url_route']['kwargs']['conversation_id']

#         await self.accept()

#         await self.send_initial_data()



#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         pass

#     @sync_to_async
#     def get_messages(self, conversation):
#         messages = Message.objects.filter(conversation=self.group_name).order_by('timestamp')
#         if messages:
#             return [{
#                 'sender': msg.sender.username,
#                 'sender_id' : msg.sender.pk,
#                 'sender_image': msg.sender.image.url if msg.sender.image else None,
#                 'sender_full_name' : msg.sender.full_name if msg.sender.full_name else None,

#                 'receiver': msg.receiver.username,
#                 'receiver_id' : msg.receiver.pk,
#                 'receiver_full_name' : msg.receiver.full_name if msg.receiver.full_name else None,

#                 'message': msg.message,
#                 'timestamp': msg.timestamp.strftime("%I:%M %p %d-%b-%y")
#             } for msg in messages]
        
#         return None
    
#     async def send_initial_data(self):
#         messages = await self.get_messages(self.group_name)
#         receiver = await self.get_receiver()
#         await self.send(text_data=json.dumps({
#             'type': 'initial_messages',
#             'messages': messages,
#             'receiver': receiver
#         }))

    
#     @sync_to_async
#     def get_receiver(self):
#         conversation = Conversation.objects.get(pk = self.group_name)
#         for participant in conversation.participants.all():
#             if participant != self.scope['user']:
#                 receiver = participant.full_name
#                 return receiver
            
#         return None
        
