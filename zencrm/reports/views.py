from django.shortcuts import render
from common.mixins import CrmLoginRequiredMixin
from django.views.generic import ListView
from .models import Report

class BaseReportView(CrmLoginRequiredMixin):
    login_url = 'login'
    model = Report


class ReportListView(BaseReportView, ListView):
    template_name = "reports/reports.html"
    queryset = Report.objects.all()