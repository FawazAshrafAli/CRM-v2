from django.urls import path
from .views import LandingPageView, SuccessView, ApplicationView

app_name = "landing"

urlpatterns = [
    path('', LandingPageView.as_view(), name="landing"),
    path('application/', ApplicationView.as_view(), name="application"),
    path('success/', SuccessView.as_view(), name="success"),
]
