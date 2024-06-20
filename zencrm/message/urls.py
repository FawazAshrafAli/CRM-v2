from django.urls import path
from .views import MessageListView, CreateMessageView, index

app_name = "messages"

urlpatterns = [
    path('', MessageListView.as_view(), name="list"),
    path('index/', index, name="index"),
    path('create/', CreateMessageView.as_view(), name="create"),

]
