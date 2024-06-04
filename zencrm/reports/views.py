from django.shortcuts import render, get_object_or_404
from common.mixins import CrmLoginRequiredMixin
from django.views.generic import ListView
from django.http import Http404

from crm_admin.models import Customer
from .models import Report

class BaseReportView(CrmLoginRequiredMixin):
    login_url = 'login'
    model = Report

    def get_context_data(self, **kwargs):
        try:
            context = {"customer": get_object_or_404(Customer, organization_id = self.request.user.organization_id)}
        except Http404:
            pass
        return context


class ReportListView(BaseReportView, ListView):
    template_name = "reports/reports.html"
    queryset = Report.objects.all()