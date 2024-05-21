from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.generic import View, ListView, CreateView, DeleteView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from pycountry import countries

from .models import Customer, Plan
from authentication.models import User, CrmUserFamilyInformation, CrmUserEducation, CrmUserExperience

class AdminBaseView(LoginRequiredMixin):
    login_url = 'authentication:login'
    success_url = reverse_lazy('crm_admin:admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["plans"] = Plan.objects.all().order_by("duration")
        return context

class CreateCustomerView(AdminBaseView, CreateView):
    model = Customer
    fields = ["name", "organization", "type_of_organization", "no_of_users", "phone", "email", "plan"]
    
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
        return super().form_valid(form)


class CustomerListView(AdminBaseView, ListView):
    model = Customer
    template_name = "admin/admin.html"
    queryset = model.objects.all()
    context_object_name = "customers"


class CustomerDetailView(AdminBaseView, DetailView):
    model = Customer

    def render_to_response(self, context):
        customer = context['object']
        serialized_data = {}

        for field in customer._meta.fields:
            field_name = field.name
            field_value = getattr(customer, field_name)
            if field_value:
                if field_name in ["logo", "favicon"]:
                    serialized_data[field_name] = field_value.url
                elif field_name == "created":
                    serialized_data[field_name] = field_value.strftime('%d-%m-%Y')
                else:    
                    serialized_data[field_name] = field_value

        if customer.expiry_date:
            serialized_data['expiry_date'] = customer.expiry_date.strftime('%d-%m-%Y')

        return JsonResponse(serialized_data)
            

class UpdateCustomerView(AdminBaseView, UpdateView):
    model = Customer
    fields = ["name", "organization", "logo", "type_of_organization", "no_of_users", "phone", "email", "plan", "website_name", "favicon"]
    

    def form_valid(self, form):
        messages.success(self.request, 'Successfully updated customer details.')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error on field {field}: {error}")
        return super().form_invalid(form)
    

class ActivateCustomerView(AdminBaseView, UpdateView):
    model = Customer
    fields = ['plan', 'active']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        plan = request.POST.get('plan')

        if plan:
            self.object.plan = plan
            self.object.active = True
            self.object.save()

            messages.success(self.request, 'Activated customer successfully.')
            return redirect(self.get_success_url())
        else:
            messages.warning(self.request, 'Please select a plan.')
            return redirect(reverse_lazy('crm_admin:admin'))
    

class DeactivateCustomer(AdminBaseView, UpdateView):
    model = Customer
    fields = ['active']

    def form_valid(self, form):
        messages.success(self.request, 'Customer deactivation successfull.')
        return super().form_valid(form)
    

class DeleteCustomerView(AdminBaseView, View):
    
    def get(self, request, *args, **kwargs):
        try:
            self.object = get_object_or_404(Customer, pk = self.kwargs['pk'])
            self.users_list = get_list_or_404(User, organization_id = self.object.organization_id)
            organization_name = self.object.organization
        except Http404:
            return redirect(self.error404)
        for user in self.users_list:
            user.delete()
        self.object.delete()
        messages.success(self.request, f'Successfully Removed all the accounts related to the organization {organization_name} from the system.')
        return redirect(self.success_url)


@method_decorator(never_cache, name='dispatch')
class UserBaseView(LoginRequiredMixin):
    login_url = 'authentication:login'
    model = User
    template_name = 'admin/users.html'
    success_url = reverse_lazy('crm_admin:users')

    error404 = reverse_lazy('authentication:error404')
    error500 = reverse_lazy('authentication:error500')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers_by_organization'] = Customer.objects.all().order_by("organization")
        context['countries'] = sorted(list(country.name for country in countries))
        return context


class CreateUserView(UserBaseView, CreateView):
    model = User
    fields = ["organization", "organization_id", "first_name", "last_name", "phone", "email", "title", "team"]

    def post(self, request, *args, **kwargs):
        customer = request.POST.get("customer")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        title = request.POST.get("title")
        team = request.POST.get("team")

        email_exists = User.objects.filter(email = email).exists()
        phone_exists = User.objects.filter(phone = phone).exists()

        if email_exists:
            messages.warning(self.request, "User with same email already exists. Please try with a different email address.")
            return redirect(reverse_lazy('crm_admin:users'))
        
        if phone_exists:
            messages.warning(self.request, "User with same phone number already exists. Please try with a different phone number.")
            return redirect(reverse_lazy('crm_admin:users'))

        try:
            self.object = get_object_or_404(Customer, pk = customer)
        except Http404:
            return redirect(self.error404)
        
        current_no_of_users = User.objects.filter(organization_id = self.object.organization_id).count()

        try:
            while self.object.no_of_users <= current_no_of_users + 1:
                self.object.no_of_users += 1
                self.object.save()

            User.objects.create(
                username = email,
                organization = self.object.organization,
                organization_id = self.object.organization_id,
                first_name = first_name,
                last_name = last_name,
                phone = phone,
                email = email,
                title = title,
                team = team,
                password = make_password(self.object.organization_id)
                )
            
            subject = "ZENCRM User Account Created"
            user_creation_message = f"""You have been added to your organization {self.object.organization}'s crm system.
                        The current username for your account is your email id and the password is {self.object.organization_id}.
                        You can change both the username and password later from your account settings."""
            html_content = render_to_string('landing_email_templates/user_registration_response.html', {
                'subject': subject,
                'message': user_creation_message,
                "email_subject": subject,
                "email_content": user_creation_message,
                "name": f"{first_name} {last_name}",
                "username": email,
                "organization": self.object.organization,
                "password": self.object.organization_id
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
        except Exception as e:
            print(F"Exception: {e}")
            return redirect(self.error500)
        
        messages.success(self.request, f"User created successfully for organization '{self.object.organization}'.")
        return redirect(self.get_success_url())
    
    def form_invalid(self, form):
        for field, errors in form.errors.fields():
            for error in errors:
                print(f"Error in fieldm, {field}: {error}")
        return super().form_invalid(form)


class UserListView(UserBaseView, ListView):
    model = User
    queryset = User.objects.all().exclude(username = 'admin').order_by("organization")
    template_name = 'admin/users.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customers'] = Customer.objects.all().order_by("name"),
        return context
    

class UpdateUserView(UserBaseView, UpdateView):
    model = 


class UserDetailView(UserBaseView, DetailView):

    def render_to_response(self, context):
        user = context['object']

        serialized_data = {}

        for field in user._meta.fields:
            field_name = field.name
            field_value = getattr(user, field_name)
            if field_value:
                if field_name == 'image':
                    serialized_data[field_name] = field_value.url
                elif field_name in ['first_name', 'last_name']:
                    if field_name == 'first_name':
                        serialized_data['full_name'] = field_value
                    else:
                        serialized_data['full_name'] += f' {field_value}'
                    serialized_data[field_name] = field_value
                elif field_name in ['address', 'address_city', 'address_state', 'address_postal_code', 'address_country']:        
                    serialized_data[field_name] = field_value
                    if field_name != 'address_country':
                        if field_name == 'address':
                            full_address = ''
                            full_address = field_value
                        else:
                            full_address += f', {field_value}'
                    else:
                        full_address += f' {field_value}'
                        serialized_data['full_address'] = full_address
                elif field_name == 'reports_to':
                    if field_value.last_name:
                        serialized_data[field_name] = f"{field_value.first_name} {field_value.last_name}"
                    else:
                        serialized_data[field_name] = field_value.first_name   
                    serialized_data[field_name + '_id'] = field_value.pk
                elif field_name in ['created', 'last_login', 'date_joined', 'updated']:
                    serialized_data[field_name] = field_value.strftime('%d-%m-%Y %H:%M %p')
                else:    
                    serialized_data[field_name] = field_value


        serialized_data.update({
            'family_member_data': list(CrmUserFamilyInformation.objects.filter(crm_user_id = user.id).values('name', 'relationship', 'date_of_birth', 'phone')),
            'educational_information_data': list(CrmUserEducation.objects.filter(crm_user_id = user.id).values('institution', 'course', 'started_year', 'completed_year')),
            'experience_data': list(CrmUserExperience.objects.filter(crm_user_id = user.id).values('designation', 'company', 'started_month_and_year', 'completed_month_and_year')),
            })
        

        return JsonResponse(serialized_data, safe=False)


@method_decorator(never_cache, name='dispatch')
class PlanBaseView(LoginRequiredMixin):
    login_url = 'authentication:login'
    model = Plan
    template_name = 'admin/plan.html'
    success_url = reverse_lazy('crm_admin:plans')

    error404 = reverse_lazy('authentication:error404')

class PlanListView(PlanBaseView, ListView):
    queryset = Plan.objects.all().order_by("duration")
    template_name = 'admin/plan.html'
    context_object_name = 'plans'


class CreatePlanView(PlanBaseView, CreateView):
    fields = ["name", "duration"]
    success_url = reverse_lazy('crm_admin:plans')

    def form_valid(self, form):
        messages.success(self.request, 'Plan creation successfull.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error on field {field}: {error}")
        return super().form_invalid(form)
    

class PlanDetailView(PlanBaseView, DetailView):
    model = Plan

    def render_to_response(self, context):
        plan = context['object']

        serialized_data = {}

        for field in plan._meta.fields:
            serialized_data[field.name] = getattr(plan, field.name)

        return JsonResponse(serialized_data)
    
class UpdatePlanView(PlanBaseView, UpdateView):
    fields = ["name", "duration"]

    def form_valid(self, form):
        messages.success(self.request, 'Plan updation successfull.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error on field {field}: {error}")
        return super().form_invalid(form)
    

class DeletePlanView(PlanBaseView, View):
    
    def get(self, request, *args, **kwargs):
        try:
            self.object = get_object_or_404(Plan, pk = self.kwargs['pk'])
        except Http404:
            return redirect(self.error404)
        self.object.delete()
        messages.success(self.request, 'Plan deletion successfull.')
        return redirect(self.success_url)