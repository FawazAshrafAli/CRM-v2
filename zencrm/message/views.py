from django.forms import BaseModelForm
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView
from common.mixins import CrmLoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .models import Message, Conversation
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
        context['users'] = User.objects.filter(organization_id = self.request.user.organization_id).exclude(id = self.request.user.id)

        context['conversations'] = Conversation.objects.all()

        return context


class CreateConversationView(CrmLoginRequiredMixin, CreateView):
    model = Conversation
    fields = "__all__"
    success_url = reverse_lazy('messages:list')

    def post(self, request, *args, **kwargs):
        participants = request.POST.getlist('participants')
        if len(participants) > 0:

            if len(participants) == 1:
                # conversation_name = User.objects.get(pk = participants[0]).username

                participants.append(request.user.pk)
                participants = sorted(participants, key=lambda x: int(x))

                conversation = Conversation.objects.filter(participants = participants[0]).filter(participants = participants[1]).first()
                print("Conversation already exists.")

                if not conversation:
                    conversation = Conversation.objects.create()
                    conversation.participants.set(participants)        
                    print("Conversation creation successfull")

                return redirect(self.success_url)
            else:
                pass
        
        else:
            messages.error(request, "please select atleast one participant")
            return redirect(reverse_lazy('messages:list'))
        


class ConversationDetailView(CrmLoginRequiredMixin, DetailView):
    model = Conversation
    context_object_name = 'conversation'
    template_name = 'message/chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['conversation'] = get_object_or_404(Conversation, pk = self.kwargs['conversation_id'])
        except Http404:
            pass
        return context