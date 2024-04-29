from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Customer

class AdminBaseView(LoginRequiredMixin):
    login_url = 'authentication:login'


class CustomerListView(AdminBaseView, ListView):
    model = Customer
    template_name = "admin/admin.html"
    queryset = model.objects.all()
    context_object_name = "customers"