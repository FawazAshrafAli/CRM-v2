from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from common.mixins import CrmLoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Message
from authentication.models import User


class BaseMessageView(CrmLoginRequiredMixin):
    model = Message
    login_url = 'authentication:login'
    template_name = "message/messages.html"
    

class MessageListView(CrmLoginRequiredMixin, ListView):
    queryset = Message.objects.all()
    template_name = "message/messages.html"
    context_object_name = 'text_messages'

    def get_queryset(self, **kwargs):
        return Message.objects.filter(sender = self.request.user) | Message.objects.filter(receiver = self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.filter(organization_id = self.request.user.organization_id)

        messages = Message.objects.filter(Q(sender = self.request.user) | Q(receiver = self.request.user))
        conversations = list(set(message.conversation for message in messages))
        print(conversations)

        return context


def index(request):
    return render(request, 'message/index.html')
