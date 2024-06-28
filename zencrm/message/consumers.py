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

        print("\nInitial values")
        print("Sender: ", self.sender)
        print("Receiver: ", self.receiver)


        self.room_group_name = f"chat_{min(self.sender, self.receiver)}_{max(self.sender, self.receiver)}"

        await self.get_user_objects()

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        self.conversation, just_created = await self.get_conversation()


        if just_created == True:
            await self.send_initial_data()

        else:
            messages = await self.unpack_conversation()
            await self.send(text_data=json.dumps({
                'type': 'conversation_history',
                'messages': messages,
                'conversation_id': self.conversation.pk
            }))

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("New Message ", message)

        await self.save_message(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @sync_to_async
    def get_user_objects(self):
        print("\nValues inside Get User Object")
        print("Sender: ", self.sender)
        print("Receiver: ", self.receiver)
        self.sender_obj = User.objects.get(pk = self.sender)
        self.receiver_obj = User.objects.get(pk = self.receiver)

    @sync_to_async
    def get_conversation(self):
        try:
            print("\nInside Get Conversation.")
            print("Sender Object: ", self.sender_obj)
            print("Receiver Object: ", self.receiver_obj)                        
            conversation = Conversation.objects.filter(participants=self.sender_obj).filter(participants=self.receiver_obj).first()

            print("Conversation Id: ", conversation.pk)

            just_created = False

            if not conversation:
                participants = sorted([self.sender_obj, self.receiver_obj], key=lambda x: x.pk)

                conversation = Conversation.objects.create()
                conversation.participants.set(participants)
                conversation.save()

                just_created = True

            return conversation, just_created
        except Exception as e:
            print(f"Exception at get_conversation: {e}")
            return None, False
        
    @sync_to_async
    def unpack_conversation(self):
        messages = Message.objects.filter(conversation = self.conversation)
        messages_list = []
        for message in messages:

            sender_id = message.sender.pk
            receiver_id = message.receiver.pk

            sender = message.sender.full_name
            receiver = message.receiver.full_name
            timestamp = message.timestamp.strftime("%I:%M %p %d-%b-%y")

            message = message.message


            messages_list.append({
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "sender": sender,
                "receiver": receiver,
                "message": message,
                "timestamp": timestamp,
            })

        return messages_list



    
    @database_sync_to_async
    def save_message(self, message):
        participants = sorted([self.sender_obj, self.receiver_obj], key=lambda x: x.pk)
        conversation = Conversation.objects.filter(participants = participants[0]).filter(participants = participants[1]).first()
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.set(participants)
            conversation.save()
        
        message = Message.objects.create(conversation = conversation, sender = self.sender_obj, receiver = self.receiver_obj, message = message)

        self.message_data =  {
            'sender_id': message.sender.pk, 
            'receiver_id': message.receiver.pk, 
            'sender': message.sender.full_name, 
            'receiver': message.receiver.full_name,  
            'sender_image': message.sender.image.url if message.sender.image else None, 
            'receiver_image': message.receiver.image.url if message.receiver.image else None,
            'timestamp': message.timestamp.strftime("%I:%M %p %d-%b-%y"),
            'message': message.message, 
            'conversation_id': conversation.pk
            }

    async def chat_message(self, event):
        message = event['message']
        
        if message:
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': self.message_data
            }))

    async def send_initial_data(self):        
        await self.send(text_data = json.dumps({
                'type': 'conversation_data',
                'conversation_id': self.conversation.pk,
                'receiver_id': self.receiver_obj.pk,
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
        
