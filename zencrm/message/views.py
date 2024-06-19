from django.shortcuts import render
from django.views.generic import ListView
from common.mixins import CrmLoginRequiredMixin

from .models import Message


class BaseMessageView(CrmLoginRequiredMixin):
    model = Message
    

class MessageListView(CrmLoginRequiredMixin, ListView):
    queryset = Message.objects.all()
    template_name = "message/messages.html"


def chat_room(request, room_name):
    return render(request, 'message/chat_room.html', {
        'room_name': room_name,
        'username': request.user.username,
    })
