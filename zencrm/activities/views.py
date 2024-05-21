from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Activity
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


@method_decorator(never_cache, name='dispatch')
class BaseActivityView(LoginRequiredMixin):
    login_url = 'authentication:login'
    model = Activity
    template_name = "activities/activities.html"


class ActivityListView(BaseActivityView, ListView):    
    queryset = Activity.objects.all()


class ActivityCreateView(BaseActivityView, DetailView):
    fields = "__all__"