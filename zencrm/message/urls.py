from django.urls import path
from .views import MessageListView, CreateConversationView, ConversationDetailView

app_name = "messages"

urlpatterns = [
    path('', MessageListView.as_view(), name="list"),
    path('create/', CreateConversationView.as_view(), name="create"),
    path('chat/<int:pk>', ConversationDetailView.as_view(), name="chat")

]
