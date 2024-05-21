from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from crm_admin.models import Customer
from django.urls import reverse_lazy
from authentication.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class LandingPageView(TemplateView):
    template_name = 'landing/landing.html'


class SuccessView(TemplateView):
    template_name = 'landing/success.html'


class ApplicationView(CreateView):
    model = Customer
    template_name = 'landing/application.html'
    fields = ["name", "organization", "type_of_organization", "plan", "no_of_users", "phone", "email", "amount"]
    success_url = reverse_lazy("landing:success")


    def form_valid(self, form):
        phone_number = form.cleaned_data.get('phone', None)
        email_id = form.cleaned_data.get('email', None)

        customer_number_exists = Customer.objects.filter(phone = phone_number).exists()
        user_number_exists = User.objects.filter(phone = phone_number).exists()

        if customer_number_exists or user_number_exists:
            messages.error(self.request, "Account with this phone number already exists.")
            return redirect(reverse_lazy("landing:application"))
        
        customer_email_exists = Customer.objects.filter(email = email_id).exists()
        user_email_exists = User.objects.filter(email = email_id).exists()

        if customer_email_exists or user_email_exists:
            messages.error(self.request, "Account with this email id already exists.")
            return redirect(reverse_lazy("landing:application"))
        
        super().form_valid(form)
        customer = Customer.objects.latest("created")
        password = make_password(customer.organization_id)
        for i in range(len(customer.name)):
            if customer.name[i] == " ":
                first_name = customer.name[:i]
                last_name = customer.name[i+1:]
                break
            else:
                first_name = customer.name
                last_name = None
        try:
            user = User.objects.create(
                username = customer.email,
                first_name = first_name,
                last_name = last_name,
                organization = customer.organization,
                organization_id = customer.organization_id,
                email = customer.email,
                phone = customer.phone,
                password = password,

            )
            customer.active = True
            customer.save()
        except Exception as e:
            try:
                Customer.objects.get(organization_id = customer.organization_id).delete()
            except:
                pass
            print(e)
            return redirect(reverse_lazy('authentication:error500'))

        try:
            subject = "ZENCRM Account Created"
            message = f"""ZENCRM account for your organization {user.organization} has been created.
                        The current username for your account is your email id and the password is {user.organization_id}.
                        You can change both the username and password later from your account settings."""
            html_content = render_to_string('landing_email_templates/user_registration_response.html', {
                'subject': subject,
                'message': message,
                "email_subject": subject,
                "email_content": message,
                "name": customer.name,
                "username": user.username,
                "organization": user.organization,
                "password": user.organization_id
                })            
                    

            email = EmailMessage(
                subject=subject,
                body=html_content,
                from_email="w3digitalpmna@gmail.com",
                to=["w3digitalpmna@gmail.com"]
            )
                        

            # Set the content type of the email to 'text/html'
            email.content_subtype = 'html'

            # Send the email
            email.send()

            return redirect(self.get_success_url())

        except Exception as e:
            print(e)
            return redirect(reverse_lazy('authentication:error500'))

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
        return super().form_invalid(form)
