from django.contrib.auth.mixins import  LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib.auth import logout

from crm_admin.models import Customer

class CrmLoginRequiredMixin(LoginRequiredMixin):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        else:
            is_customer_active = False
            try:
                customer = get_object_or_404(Customer, organization_id = request.user.organization_id)
                if customer.active:
                    is_customer_active = True
            except Http404:
                pass
            
            if not is_customer_active and not request.user.is_superuser:
                return redirect(reverse_lazy('authentication:expired'))
        
        return super().dispatch(request, *args, **kwargs)
            