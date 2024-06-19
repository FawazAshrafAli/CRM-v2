from django.urls import path
from .views import MessageListView, chat_room

app_name = "messages"

urlpatterns = [
    path('', MessageListView.as_view(), name="list"),
    path('chat/<str:room_name>/', chat_room, name='chat_room'),
]
