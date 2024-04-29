from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from crm_admin.models import Customer
from django.urls import reverse_lazy
from authentication.models import User
from django.contrib.auth.hashers import make_password


class LandingPageView(TemplateView):
    template_name = 'landing/landing.html'


class SuccessView(TemplateView):
    template_name = 'landing/success.html'


class ApplicationView(CreateView):
    model = Customer
    template_name = 'landing/application.html'
    fields = ["name", "organization", "logo", "type_of_organization", "no_of_users", "phone", "email", "amount"]
    success_url = reverse_lazy("landing:success")


    def form_valid(self, form):
        response = super().form_valid(form)
        customer = Customer.objects.latest("created")
        password = make_password(customer.organization_id)
        print(customer.organization_id)
        for i in range(len(customer.name)):
            if customer.name[i] == " ":
                first_name = customer.name[:i]
                last_name = customer.name[i+1:]
                break
            else:
                first_name = customer.name
                last_name = None
        User.objects.create(
            username = customer.email,
            first_name = first_name,
            last_name = last_name,
            organization = customer.organization,
            organization_id = customer.organization_id,
            email = customer.email,
            phone = customer.phone,
            password = password,

        )
        return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
        return super().form_invalid(form)
