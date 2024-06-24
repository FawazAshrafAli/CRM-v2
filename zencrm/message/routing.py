from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<sender>\w+)/(?P<receiver>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<conversation_id>\w+)/$', consumers.ConversationChatConsumer.as_asgi()),
]