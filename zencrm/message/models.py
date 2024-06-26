from django.db import models
from authentication.models import User


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Conversation'

    def __str__(self):
        self.sorted_participants = sorted(list(self.participants.all()), key = lambda x: x.pk)
        return f"Conversation between {", ".join([user.username for user in self.sorted_participants])}"
    
    def last_message(self):
        message = Message.objects.filter(conversation = self).last()
        return message.message if message else None

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name="conversation", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="message_sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="message_receiver", on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Message'


    def __str__(self):
        return f'{self.sender} to {self.receiver}: {self.message[:20]}'
