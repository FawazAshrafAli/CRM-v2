from django.urls import path
from .views import (
    ActivityListView, CreateActivityView, FetchGuestView, 
    ActivityDetailView
    )

app_name = "activities"

urlpatterns = [
    path('', ActivityListView.as_view(), name="list"),
    path('create/', CreateActivityView.as_view(), name="create"),
    path('get_guests/', FetchGuestView.as_view(), name="get_guests"),    
    path('detail/<pk>', ActivityDetailView.as_view(), name="detail"),    
]
