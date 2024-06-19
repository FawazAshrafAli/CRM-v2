from django.urls import path
from .views import (
    ActivityListView, CreateActivityView, FetchGuestView, ActivityDetailView, 
    UpdateActivityView, DeleteActivityView,ClosedActivityListView, 
    OpenedActivityListView, MyActivityListView
    )

app_name = "activities"

urlpatterns = [
    path('', ActivityListView.as_view(), name="list"),
    path('closed/', ClosedActivityListView.as_view(), name="closed"),
    path('opened/', OpenedActivityListView.as_view(), name="opened"),
    path('my_activity/', MyActivityListView.as_view(), name="my_activity"),
    path('create/', CreateActivityView.as_view(), name="create"),
    path('get_guests/', FetchGuestView.as_view(), name="get_guests"),    
    path('detail/<pk>', ActivityDetailView.as_view(), name="detail"),
    path('update/<pk>', UpdateActivityView.as_view(), name="update"),
    path('delete/<pk>', DeleteActivityView.as_view(), name="delete"),
]
