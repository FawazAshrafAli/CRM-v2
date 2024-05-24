from django.urls import path
from .views import (CustomerListView, CustomerDetailView, 
                    UpdateCustomerView, ActivateCustomerView, 
                    DeactivateCustomer, PlanListView, 
                    CreatePlanView, PlanDetailView, 
                    UpdatePlanView, DeletePlanView, 
                    DeleteCustomerView, UserListView, 
                    UserDetailView, CreateCustomerView, 
                    CreateUserView, UpdateUserView)

app_name = "crm_admin"

urlpatterns = [
    path('', CustomerListView.as_view(), name="admin"),
    path('create_customer/', CreateCustomerView.as_view(), name="create_customer"),
    path('customer_detail/<pk>', CustomerDetailView.as_view(), name="customer_detail"),
    path('update_customer/<pk>', UpdateCustomerView.as_view(), name="update_customer"),
    path('activate_customer/<pk>', ActivateCustomerView.as_view(), name="activate_customer"),
    path('deactivate_customer/<pk>', DeactivateCustomer.as_view(), name="deactivate_customer"),
    path('delete_customer/<pk>', DeleteCustomerView.as_view(), name="delete_customer"),

    path('create_user/', CreateUserView.as_view(), name="create_user"),
    path('users/', UserListView.as_view(), name="users"),
    path('user_details/<pk>', UserDetailView.as_view(), name="user_details"),
    path('update_user/<pk>', UpdateUserView.as_view(), name="update_user"),

    path('plans/', PlanListView.as_view(), name="plans"),
    path('create_plan/', CreatePlanView.as_view(), name="create_plan"),
    path('plan_details/<pk>', PlanDetailView.as_view(), name="plan_details"),
    path('update_plan/<pk>', UpdatePlanView.as_view(), name="update_plan"),
    path('delete_plan/<pk>', DeletePlanView.as_view(), name="delete_plan"),
]
