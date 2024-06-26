from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from common.mixins import CrmLoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy

from authentication.models import User
from crm_admin.models import Customer

class BaseDashboardView(CrmLoginRequiredMixin):
    login_url='authentication:login'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect(reverse_lazy('crm_admin:admin'))
        else:
            return super().dispatch(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs):
        try:
            context = {"customer": get_object_or_404(Customer, organization_id = self.request.user.organization_id)}
        except Http404:
            pass
        return context


class DealsDashboardView(BaseDashboardView, TemplateView):
    template_name = 'dashboard/deals-dashboard.html'


class LeadsDashboardView(BaseDashboardView, TemplateView):    
    template_name = 'dashboard/leads-dashboard.html'


class ProjectsDashboardView(BaseDashboardView, TemplateView):    
    template_name = 'dashboard/projects-dashboard.html'

