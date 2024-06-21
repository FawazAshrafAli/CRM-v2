from django.db import models
from authentication.models import User


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation between {", ".join([user.username for user in self.participants.all()])}"

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="message_sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="message_receiver", on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def conversation(self):
        participants = sorted(([self.sender, self.receiver]), key = lambda x: x.pk)
        return f"{participants[0].username}-{participants[1].username}"


    def __str__(self):
        return f'{self.sender} to {self.receiver}: {self.message[:20]}'
