from django.urls import path
from .views import CustomerListView

app_name = "crm_user"

urlpatterns = [
    path('', CustomerListView.as_view(), name="admin"),
]
