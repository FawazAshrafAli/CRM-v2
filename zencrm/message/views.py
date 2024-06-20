from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from common.mixins import CrmLoginRequiredMixin
from django.urls import reverse_lazy

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
        return context

class CreateMessageView(CrmLoginRequiredMixin, CreateView):
    success_url = reverse_lazy('messages:list')

    def post(self, request, *args, **kwargs):
        pass
        # message = request.POST.get('message')
        # sender = request.user
        # receiver = User.objects.get(first_name = "Robert", last_name = "Wald")

        # Message.objects.create(content = message, sender = sender, receiver = receiver)

        # return redirect(self.success_url)


def index(request):
    return render(request, 'message/index.html')
