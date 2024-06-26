from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (TemplateView, DetailView, 
                                  UpdateView, CreateView, 
                                  DeleteView)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from common.mixins import CrmLoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.core.mail import EmailMessage
from django.views.generic import View
from django.contrib import messages
from django.http import Http404
from datetime import datetime
from random import randrange

from crm_admin.models import Customer, Plan
from .models import User, CrmUserFamilyInformation, CrmUserEducation, CrmUserExperience, UserOtp


@method_decorator(never_cache, name="dispatch")
class ExpiredTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'authentication/expired.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plans'] = Plan.objects.all().order_by('duration')
        try:
            context['customer'] = get_object_or_404(Customer, organization_id = self.request.user.organization_id)
        except Http404:
            pass
        return context


# @method_decorator(never_cache, name='dispatch')
# class RegisterUserView(TemplateView):
#     template_name = 'authentication/register.html'

#     def post(self, request, *args, **kwargs):
#         if request.method != "POST":
#             return redirect(reverse_lazy("authentication:error500"))
            
#         context = {}
#         message = None

#         first_name = request.POST.get("first_name")
#         last_name = request.POST.get("last_name")
#         username = request.POST.get("username")
#         email = request.POST.get("email")        
#         password = request.POST.get("password")
#         repeat_password = request.POST.get("repeat_password")

#         required_fields = ["first_name", "username", "email", "password", "repeat_password"]

#         for field in required_fields:
#             if not locals()[field]:
#                 message = f"{field.capitalize()} field cannot be blank"                
#                 break
#             else:
#                 context.update({str(field.lower()): locals()[field]})                

#         if not message:
#             if password != repeat_password:
#                 message = "Passwords do not match."
#                 context.update({"password": password})

#             if not message:
#                 try:
#                     hashed_password = make_password(password)
#                     user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, password=hashed_password)                                    
#                     messages.success(request, "User creation successful")
#                     login(request, user)
#                     return redirect(reverse('dashboard:deals_dashboard'))
#                 except IntegrityError:
#                     try:
#                         get_object_or_404(User, username = username)
#                         message = "User with the given username already exists."
#                     except Http404:
#                         pass
#                     try:
#                         get_object_or_404(User, email = email)
#                         message = "User with the given email already exists."
#                     except Http404:
#                         pass
#                     context.update({"repeat_password": repeat_password})

#         if message:
#             messages.error(request, message)        
#         return render(request, self.template_name, context)

class LoginView(TemplateView):
    template_name = 'authentication/login.html'
    success_url = reverse_lazy('dashboard:deals_dashboard')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:            
            return redirect(self.success_url)
        else:            
            return render(request, self.template_name)   

    def post(self, request, *args, **kwargs):
        if request.method != "POST":
            return redirect(reverse_lazy("authentication:error500"))

        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('dashboard:deals_dashboard'))                    
            else:
                messages.error(request, 'Invalid username or password')                

        return render(request, self.template_name)

        
class LogoutView(LoginRequiredMixin, View):
    login_url = 'authentication:login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('authentication:login'))


@method_decorator(csrf_exempt, name='dispatch')
class ForgotPasswordView(View):

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')

        if not email:
            return JsonResponse({'message': 'Email is required'}, status=400)
        
        valid_user = False
        try:
            self.user = get_object_or_404(User, email = email)
            valid_user = True
            otp = randrange(100000, 1000000)
            UserOtp.objects.update_or_create(email = email, defaults = {'otp': otp})

            self.otp_object = get_object_or_404(UserOtp, email = email)

            subject = "OTP FOr Resetting Password"
            message = f"""OTP for resetting your crm user account is {self.otp_object.otp}.
                    Submit this OTP along with your new password to reset your password."""
            html_content = render_to_string('authentication_email_template/email_otp.html', {
                'subject': subject,
                'message': message,
                "email_subject": subject,
                "email_content": message,
                "name": self.user.first_name,
                "otp": self.otp_object.otp,                    
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

            return JsonResponse({'message': 'Mailed OTP'})

        except Http404:
            if valid_user:
                return JsonResponse({'message': 'Invalid OTP'}, status=403)
            else:
                return JsonResponse({'message': 'Invalid User'}, status=403)                
    
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'message': 'Server Error'}, status=500)
        

class ResetPasswordView(UpdateView):
    model = User
    pk_url_kwarg = 'email'
    fields = ["password"]
    success_url = reverse_lazy('authentication:login')

    def get_object(self, **kwargs):
        try:
            return get_object_or_404(User, email = self.kwargs['email'])
        except Http404:
            pass

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        repeat_password = request.POST.get('repeat_password')

        try:
            get_object_or_404(UserOtp, email = self.object.email, otp = otp)
            if new_password == repeat_password:
                password = make_password(new_password)
                self.object.password = password
                self.object.save()
                messages.success(self.request, 'Successfully resetted password.')
                return redirect(self.get_success_url())
            else:
                return JsonResponse({'error': 'Error', 'message': 'Passwords not matching'}, status=403)
        except Http404:
            return JsonResponse({'error': 'Error', 'message': 'Invalid OTP'}, status=403)    
    
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': 'Error','message': 'Server Error'}, status=500)



class RenewAccountView(LoginRequiredMixin, UpdateView):    
    model = Customer
    fields = ['plan', 'no_of_users', 'active']
    success_url = reverse_lazy('dashboard:deals_dashboard')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        plan = request.POST.get('plan')
        no_of_users = request.POST.get('no_of_users')

        if plan and no_of_users:
            self.object.plan = plan
            self.object.no_of_user = no_of_users
            self.object.active = True
            self.object.save()

            messages.success(self.request, 'Congratulations. Your CRM account has been successfully reactivated.')
            return redirect(self.get_success_url())
        else:
            if not plan:
                messages.warning(self.request, 'Please select a plan.')
            elif not no_of_users:
                messages.warning(self.request, 'Please provide the number of users.')
            else:
                messages.warning(self.request, 'Please select a plan and provide the number of users.')
            return redirect(reverse_lazy('authentication:expired'))
        
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error on field, {field}: {error}")
        return super().form_invalid(form)




class BaseCrmUserView(CrmLoginRequiredMixin):
    login_url = "authentication:login"
    model = User
    error404 = reverse_lazy('authentication:error404')
    error500 = reverse_lazy('authentication:error500')

    def get_context_data(self, **kwargs):
        try:
            context = {"customer": get_object_or_404(Customer, organization_id = self.request.user.organization_id)}
        except Http404:
            pass
        return context

class CrmUserDetailView(BaseCrmUserView, DetailView):    
    context_object_name = "user"

    def render_to_response(self, context, **response_kwargs):
        user = context['object']

        serialized_data = {}
        
        for field in user._meta.fields:            
            field_name = field.name
            field_value = getattr(user, field_name)
            if field_value:
                print(field_name, ": ", field_value)
                if field_name in ["first_name", "last_name"]:
                    serialized_data[field_name] = field_value
                    if field_name == 'first_name':
                        serialized_data["full_name"] = field_value                    
                    elif field_name == 'last_name':
                        serialized_data["full_name"] += f" {field_value}"
                
                elif field_name == 'image':
                    serialized_data[field_name] = field_value.url

                elif field_name == "reports_to":
                    if field_value.last_name:
                        field_value = f"{field_value.first_name} {field_value.last_name}"
                    else:
                        field_value = field_value.first_name
                    
                    serialized_data[field_name] = field_value

                elif field_name in ('created', 'updated'):
                    serialized_data[field_name] = field_value.strftime("%b %d, %Y")
                else:                
                    serialized_data[field_name] = field_value            

        return JsonResponse(serialized_data)
    

class CrmUserUpdateView(BaseCrmUserView, View):
    model = User
    fields = "__all__"
    success_url = reverse_lazy('authentication:my_profile')
    redirect_url = success_url

    def post(self, request, *args, **kwargs):
        if request.method != "POST":
            return redirect(self.error500)

        try:
            self.object = get_object_or_404(User, pk = self.request.user.pk)
        except Http404:
            return redirect(reverse_lazy('authentication:error404'))

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        image = request.FILES.get('image')
        title = request.POST.get('title')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        birthday = request.POST.get('birthday')
        gender = request.POST.get('gender')
        team = request.POST.get('team')
        reports_to = request.POST.get('reports_to')
        try:
            reports_to = get_object_or_404(User, pk = reports_to)
        except Http404:
            pass
        address = request.POST.get('address')
        address_city = request.POST.get('address_city')
        address_state = request.POST.get('address_state')
        address_postal_code = request.POST.get('address_postal_code')
        address_country = request.POST.get('address_country')

        self.object.first_name = first_name
        self.object.last_name = last_name
        if image:
            self.object.image = image
        self.object.title = title
        self.object.phone = phone
        self.object.email = email
        self.object.birthday = birthday
        self.object.gender = gender
        self.object.team = team
        self.object.reports_to = reports_to
        self.object.address = address
        self.object.address_city = address_city            
        self.object.address_state = address_state    
        self.object.address_postal_code = address_postal_code    
        self.object.address_country = address_country            
        
        try:
            self.object.save()
            messages.success(self.request, 'User details successfully updated.')
            return redirect(self.success_url)
        except Exception as e:
            print(e)
            return redirect(reverse_lazy('authentication:error500'))


class CrmUserPersonalInfoUpdateView(BaseCrmUserView, View):
    model = User
    fields = [
        "passport_number", "passport_expiry_date", "tel", 
        "nationality", "religion", "marital_status", 
        "employment_of_spouse", "number_of_children", 
    ]
    success_url = reverse_lazy('authentication:my_profile')
    redirect_url = success_url

    def post(self, request, *args, **kwargs):
        if request.method != "POST":
            return redirect(self.error500)

        try:
            self.object = get_object_or_404(User, pk = self.request.user.pk)
        except Http404:
            return redirect(reverse_lazy('authentication:error404'))
        
        passport_number = request.POST.get('passport_number')
        passport_expiry_date = request.POST.get('passport_expiry_date')
        tel = request.POST.get('tel')
        nationality = request.POST.get('nationality')
        religion = request.POST.get('religion')
        marital_status = request.POST.get('marital_status')
        employment_of_spouse = request.POST.get('employment_of_spouse')
        number_of_children = request.POST.get('number_of_children', 0)

        self.object.passport_number = passport_number
        self.object.passport_expiry_date = passport_expiry_date
        self.object.tel = tel
        self.object.nationality = nationality
        self.object.religion = religion
        self.object.marital_status = marital_status
        self.object.employment_of_spouse = employment_of_spouse
        self.object.number_of_children = number_of_children

        try:
            self.object.save()
            messages.success(self.request, "Updated your personal information.")
            return redirect(self.success_url)
        except Exception as e:
            print(e)
            return redirect(reverse_lazy('authentication:error500'))


class CrmUserEmergencyContactUpdateView(BaseCrmUserView, View):
    model = User
    fields = [
        "primary_contact_name", "primary_contact_relationship", 
        "primary_contact_phone1", "primary_contact_phone2", 
        "secondary_contact_name", "secondary_contact_relationship", 
        "secondary_contact_phone1", "secondary_contact_phone2"
    ]
    success_url = reverse_lazy('authentication:my_profile')
    redirect_url = success_url

    def post(self, request, *args, **kwargs):
        if request.method != "POST":
            return redirect(self.error500)

        try:
            self.object = get_object_or_404(User, pk = self.request.user.pk)
        except Http404:
            return redirect(reverse_lazy('authentication:error404'))
        
        primary_contact_name = request.POST.get('primary_contact_name')
        primary_contact_relationship = request.POST.get('primary_contact_relationship')
        primary_contact_phone1 = request.POST.get('primary_contact_phone1')
        primary_contact_phone2 = request.POST.get('primary_contact_phone2')
        secondary_contact_name = request.POST.get('secondary_contact_name')
        secondary_contact_relationship = request.POST.get('secondary_contact_relationship')
        secondary_contact_phone1 = request.POST.get('secondary_contact_phone1')
        secondary_contact_phone2 = request.POST.get('secondary_contact_phone2')
                
        self.object.primary_contact_name = primary_contact_name
        self.object.primary_contact_relationship = primary_contact_relationship
        self.object.primary_contact_phone1 = primary_contact_phone1
        self.object.primary_contact_phone2 = primary_contact_phone2
        self.object.secondary_contact_name = secondary_contact_name
        self.object.secondary_contact_relationship = secondary_contact_relationship
        self.object.secondary_contact_phone1 = secondary_contact_phone1
        self.object.secondary_contact_phone2 = secondary_contact_phone2

        try:
            self.object.save()
            messages.success(self.request, "Updated your emergency contact informations.")
            return redirect(self.success_url)
        except Exception as e:
            print(e)
            return redirect(reverse_lazy('authentication:error500'))
        

class CrmUserBankInfoUpdateView(BaseCrmUserView, View):
    model = User
    fields = [
        "bank_name", "bank_account_number", 
        "ifsc_code", "pan_number"
    ]
    success_url = reverse_lazy('authentication:my_profile')

    def post(self, request, *args, **kwargs):
        if request.method != "POST":
            return redirect(self.error500)

        try:
            self.object = get_object_or_404(User, pk = self.request.user.pk)
        except Http404:
            return redirect(reverse_lazy('authentication:error404'))
        
        bank_name = request.POST.get('bank_name')
        bank_account_number = request.POST.get('bank_account_number')
        ifsc_code = request.POST.get('ifsc_code')
        pan_number = request.POST.get('pan_number')        
                
        self.object.bank_name = bank_name
        self.object.bank_account_number = bank_account_number
        self.object.ifsc_code = ifsc_code
        self.object.pan_number = pan_number        

        try:
            self.object.save()
            messages.success(self.request, "Successfully updated your bank informations.")
            return redirect(self.success_url)
        except Exception as e:
            print(e)
            return redirect(reverse_lazy('authentication:error500'))
        

class CrmUserFamilyUpdationView(BaseCrmUserView, CreateView):
    model = User
    fields = ["family_info"]
    success_url = reverse_lazy('authentication:my_profile')

    def get_object(self, **kwargs):
        try:
            return get_object_or_404(User, pk = self.request.user.pk)
        except Http404:
            return redirect(reverse_lazy('authentication:error404'))

    def post(self, request, *args, **kwargs):
        if request.method != "POST":
            return redirect(self.error500)

        self.object = self.get_object()

        name = request.POST.get('name')
        relationship = request.POST.get('relationship')
        date_of_birth = request.POST.get('date_of_birth')
        phone = request.POST.get('phone')        

        try:
            family_info_object = get_object_or_404(CrmUserFamilyInformation, crm_user_id = self.object.pk, name = name)
        except Http404:
            kwargs = {
                'crm_user_id' : self.object.pk,
                'name' : name,
                'relationship' : relationship,
                'date_of_birth' : date_of_birth,
                'phone' : phone
            }            
            family_info_object = CrmUserFamilyInformation.objects.create(**kwargs)        

        if family_info_object not in self.object.family_info.all():
            self.object.family_info.add(family_info_object)
            self.object.save()
            messages.success(self.request, "Family member added successfully.")
            return redirect(self.get_success_url())
        else:
            messages.error(self.request, "Member already exists in your family info.")
            return redirect(self.get_success_url())
    
    def form_valid(self, form):
        messages.success(self.request, "Family member added successfully.")
        return super().form_invalid(form)
    

class CrmUserEducationUpdationView(BaseCrmUserView, UpdateView):
    model = User
    fields = ["education_info"]
    success_url = reverse_lazy('authentication:my_profile')

    def get_object(self, **kwargs):
        try:
            return get_object_or_404(User, pk = self.request.user.pk)
        except Http404:
            return redirect(reverse_lazy('authentication:error404'))

    def post(self, request, *args, **kwargs):
        if request.method != "POST":
            return redirect(self.error500)

        self.object = self.get_object()

        institution = request.POST.get('institution')
        course = request.POST.get('course')
        started_year = request.POST.get('started_year')
        completed_year = request.POST.get('completed_year')
        present = request.POST.get('present')
        
        if present != None or completed_year == None:
            completed_year = "Present"

        try:
            education_object = get_object_or_404(CrmUserEducation, crm_user_id = self.request.user.pk, course = course)
        except Http404:
            kwargs = {
                'crm_user_id' : self.object.pk,
                'institution' : institution,
                'course' : course,
                'started_year' : started_year,
                'completed_year' : completed_year
            }            
            education_object = CrmUserEducation.objects.create(**kwargs)        

        if education_object not in self.object.education_info.all():
            self.object.education_info.add(education_object)
            self.object.save()
            messages.success(self.request, "Education added successfully.")
            return redirect(self.get_success_url())
        else:
            messages.error(self.request, "Education already exists.")
            return redirect(self.get_success_url())
    
    def form_valid(self, form):
        messages.success(self.request, "Education added successfully.")
        return super().form_invalid(form)


class CrmUserExperienceUpdationView(BaseCrmUserView, CreateView):
    model = User
    fields = ["experience"]
    success_url = reverse_lazy('authentication:my_profile')

    def get_object(self, **kwargs):
        try:
            return get_object_or_404(User, pk = self.request.user.pk)
        except Http404:
            return redirect(reverse_lazy('authentication:error404'))

    def post(self, request, *args, **kwargs):
        if request.method != "POST":
            return redirect(self.error500)

        self.object = self.get_object()

        designation = request.POST.get('designation')
        company = request.POST.get('company')
        started_month_and_year = request.POST.get('started_month_and_year')
        completed_month_and_year = request.POST.get('completed_month_and_year')
        present = request.POST.get('present')
        
        if present != None or completed_month_and_year == None:
            completed_month_and_year = "Present"

        try:
            experience_object = get_object_or_404(CrmUserExperience, crm_user_id = self.object.pk, designation = designation, company = company, started_month_and_year = started_month_and_year)
        except Http404:
            kwargs = {
                'crm_user_id' : self.object.pk,
                'designation' : designation,
                'company' : company,
                'started_month_and_year' : started_month_and_year,
                'completed_month_and_year' : completed_month_and_year
            }            
            experience_object = CrmUserExperience.objects.create(**kwargs)        

        if experience_object not in self.object.experience.all():
            self.object.experience.add(experience_object)
            self.object.save()
            messages.success(self.request, "Experience added successfully.")
            return redirect(self.get_success_url())
        else:
            messages.error(self.request, "Experience already exists.")
            return redirect(self.get_success_url())
    
    def form_valid(self, form):
        messages.success(self.request, "Experience added successfully.")
        return super().form_invalid(form)


class MyProfileView(BaseCrmUserView, TemplateView):
    model = User
    template_name = "crmuser/profile.html"

    def get_object(self, **kwargs):
        return get_object_or_404(User, pk = self.request.user.pk)        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        self.object = self.get_object()        
        context.update({
            'user': self.object,    
            'users': User.objects.all()
            })
        if self.object.birthday:
            context['user_birthday'] = datetime.strptime(self.object.birthday, "%d/%m/%Y")
        return context


class FamilyMemberDetailView(BaseCrmUserView, DetailView):
    model = CrmUserFamilyInformation
    
    def get_object(self, **kwargs):
        member = super().get_object(**kwargs)
        try:
            crm_user = get_object_or_404(User, pk = self.request.user.pk)

            crm_user_family = crm_user.family_info.all()
            if member in crm_user_family:
                return member        
        except Http404:
            pass    
        return redirect(reverse_lazy('authentication:error404'))


    def render_to_response(self, context):
        member = context['object']

        serialized_data = {
            'id': member.pk,
            'name': member.name,
            'relationship': member.relationship,
            'dob': member.date_of_birth,
            'phone': member.phone
        }

        return JsonResponse(serialized_data)


class FamilyMemberUpdateView(BaseCrmUserView, UpdateView):
    model = CrmUserFamilyInformation
    fields = [
        "name", "relationship", 
        "date_of_birth", "phone" 
    ]
    success_url = reverse_lazy('authentication:my_profile')

    def get_object(self, **kwargs):
        member = super().get_object(**kwargs)
        try:
            crm_user = get_object_or_404(User, pk = self.request.user.pk)
            
            crm_user_family = crm_user.family_info.all()
            if member in crm_user_family:
                return member
        except Http404:
            pass
        
        return redirect(reverse_lazy('authentication:error404'))
    
    def form_valid(self, form):
        messages.success(self.request, "Family member updated successfully.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error on {field}: {error}")
        return super().form_invalid(form)


class FamilyMemberDeleteView(BaseCrmUserView, View):
    model = CrmUserFamilyInformation
    success_url = reverse_lazy('authentication:my_profile')

    def get(self, request, *args, **kwargs):
        try:
            self.object = get_object_or_404(CrmUserFamilyInformation, pk = self.kwargs['pk'])
        except Http404:
            return redirect(reverse_lazy('authentication:error404'))
        try:
            self.object.delete()
            messages.success(self.request, "Family member deleted successfully.")
            return redirect(self.success_url)
        except Exception as e:
            print(e)
            return redirect(reverse_lazy('authentication:error500'))


class EducationDetailView(BaseCrmUserView, DetailView):
    model = CrmUserEducation
    
    def get_object(self, **kwargs):
        education = super().get_object(**kwargs)
        try:
            crm_user = get_object_or_404(User, pk = self.request.user.pk)

            crm_user_education = crm_user.education_info.all()
            if education in crm_user_education:
                return education        
        except Http404:
            pass    
        return redirect(reverse_lazy('authentication:error404'))


    def render_to_response(self, context):
        education = context['object']

        serialized_data = {
            'id': education.pk,
            'institution': education.institution,
            'course': education.course,
            'started_year': education.started_year,
            'completed_year': education.completed_year
        }

        return JsonResponse(serialized_data)


class EducationUpdateView(BaseCrmUserView, UpdateView):
    model = CrmUserEducation
    fields = [
        "institution", "course", 
        "started_year", "completed_year" 
    ]
    success_url = reverse_lazy('authentication:my_profile')

    def get_object(self, **kwargs):
        education = super().get_object(**kwargs)
        try:
            crm_user = get_object_or_404(User, pk = self.request.user.pk)
            
            crm_user_education = crm_user.education_info.all()
            if education in crm_user_education:
                return education
        except Http404:
            pass
        
        return redirect(reverse_lazy('authentication:error404'))
    
    def form_valid(self, form):
        messages.success(self.request, "Education updated successfully.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error on {field}: {error}")
        return super().form_invalid(form)


class EducationDeleteView(BaseCrmUserView, View):
    model = CrmUserEducation
    success_url = reverse_lazy('authentication:my_profile')

    def get(self, request, *args, **kwargs):
        try:
            print(kwargs['pk'])
            self.object = get_object_or_404(CrmUserEducation, pk = self.kwargs['pk'])
        except Http404:
            return redirect(reverse_lazy('authentication:error404'))
        try:
            self.object.delete()
            messages.success(self.request, "Education deleted successfully.")
            return redirect(self.success_url)
        except Exception as e:
            print(e)
            return redirect(reverse_lazy('authentication:error500'))



class ExperienceDetailView(BaseCrmUserView, DetailView):
    model = CrmUserExperience
    
    def get_object(self, **kwargs):
        experience = super().get_object(**kwargs)
        try:
            crm_user = get_object_or_404(User, pk = self.request.user.pk)

            crm_user_experience = crm_user.experience.all()
            if experience in crm_user_experience:
                return experience        
        except Http404:
            pass    
        return redirect(reverse_lazy('authentication:error404'))


    def render_to_response(self, context):
        experience = context['object']

        serialized_data = {
            'id': experience.pk,
            'designation': experience.designation,
            'company': experience.company,
            'started_month_and_year': experience.started_month_and_year,
            'completed_month_and_year': experience.completed_month_and_year
        }

        return JsonResponse(serialized_data)
    

class ExperienceUpdateView(BaseCrmUserView, UpdateView):
    model = CrmUserExperience
    fields = [
        "designation", "company", 
        "started_month_and_year", "completed_month_and_year" 
    ]
    success_url = reverse_lazy('authentication:my_profile')

    def get_object(self, **kwargs):
        experience = super().get_object(**kwargs)
        try:
            crm_user = get_object_or_404(User, pk = self.request.user.pk)
            
            crm_user_experience = crm_user.experience.all()
            if experience in crm_user_experience:
                return experience
        except Http404:
            pass
        
        return redirect(reverse_lazy('authentication:error404'))
    
    def form_valid(self, form):
        messages.success(self.request, "Experience updated successfully.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error on {field}: {error}")
        return super().form_invalid(form)
    

class ExperienceDeleteView(BaseCrmUserView, View):
    model = CrmUserExperience
    success_url = reverse_lazy('authentication:my_profile')

    def get(self, request, *args, **kwargs):
        try:
            print(kwargs['pk'])
            self.object = get_object_or_404(CrmUserExperience, pk = self.kwargs['pk'])
        except Http404:
            return redirect(reverse_lazy('authentication:error404'))
        try:
            self.object.delete()
            messages.success(self.request, "Experience deleted successfully.")
            return redirect(self.success_url)
        except Exception as e:
            print(e)
            return redirect(reverse_lazy('authentication:error500'))


class SettingsView(BaseCrmUserView, TemplateView):
    model = User
    template_name = 'crmuser/settings.html'
    success_url = reverse_lazy('authentication:settings')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try: 
            customer = get_object_or_404(Customer, organization_id = self.request.user.organization_id)
        except Http404:
            return redirect(self.error404)
        no_of_users = User.objects.filter(organization_id = customer.organization_id).count()
        if no_of_users < customer.no_of_users:
            context['eligible_to_create'] = True
        context ['customer'] = customer
        context['users'] = User.objects.filter(organization_id = customer.organization_id)
        return context


class UpdateCustomerBasicView(SettingsView, UpdateView):
    model = Customer
    fields = ["website_name", "logo", "favicon"]

    def form_valid(self, form):
        messages.success(self.request, "Successfully updated base details of organization.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error on field {field}: {error}")
        return super().form_invalid(form)
    

class RemoveCustomerLogoView(SettingsView, UpdateView):
    model = Customer
    fields = ["logo"]
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.logo = None
        self.object.save()
        serialized_data = {
            'message': 'Success',
            }
        return JsonResponse(serialized_data)
        

class RemoveCustomerFaviconView(SettingsView, UpdateView):
    model = Customer
    fields = ["favicon"]
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.favicon = None
        self.object.save()
        serialized_data = {
            'message': 'Success',
            }
        return JsonResponse(serialized_data)


class UpdateNumberOfUsers(SettingsView, UpdateView):
    model = Customer
    fields = ['no_of_users']

    def form_valid(self, form):
        messages.success(self.request, 'Upgraded number of users.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error on field, {field}: {error}")
        return super().form_invalid(form)


class AddNewUserView(SettingsView, CreateView):
    fields = ["username", "email", "password"]
    redirect_url = reverse_lazy('authentication:settings')

    def post(self, request, *args, **kwargs):
        if request.method != "POST":
            return redirect(self.error500)

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        repeat_password = request.POST.get("repeat_password")
        if password != repeat_password:
            messages.error(self.request, "The passwords does not match.")
            return redirect(self.redirect_url)

        email_exists = User.objects.filter(email = email).exists()
        username_exists = User.objects.filter(username = username).exists()

        if email_exists:
            messages.warning(self.request, "User with similar email already exists.")
            return redirect(self.redirect_url)
        
        if username_exists:
            messages.warning(self.request, "User with similar username already exists.")
            return redirect(self.redirect_url)

        password = make_password(password)
        try:
            User.objects.create(username=username, email=email, password=password, organization_id = self.request.user.organization_id)
        except Exception as e:
            print(e)
            return redirect(self.error500)
        messages.success(self.request, "New user created successfully.")
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error on field {field}: {error}")
        return super().form_invalid(form)

class UserDetailView(SettingsView, DetailView):
    model = User
    query_pk_and_slug = 'pk'
        
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        serialized_data = {
            'username' : self.object.username,
        }
        return JsonResponse(serialized_data)


class DeleteUserView(SettingsView, View):
    def get(self, request, *args, **kwargs):
        try:
            object = get_object_or_404(User, pk = self.kwargs['pk'])
        except Http404:
            return redirect(self.error404)
        
        object.delete()
        messages.success(self.request, "Deleted user successfully.")
        return redirect(self.success_url)
    

class UpdateUsername(SettingsView, UpdateView):
    model = User
    fields = ["username"]

    def get_object(self):
        try:
            return get_object_or_404(User, pk = self.request.user.pk)
        except Http404:
            return redirect(self.error404)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Successfully updated your username.')
        return response
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error on field {field}: {error}")
        return super().form_invalid(form)
        
@method_decorator(never_cache, name='dispatch')
class ChangePassword(SettingsView, UpdateView):
    model = User
    fields = ["password"]

    def post(self, request, *args, **kwargs):
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        repeat_password = request.POST.get('repeat_password')

        user = authenticate(username=self.request.user.username, password=password)
        if user:
            if new_password == repeat_password:
                new_password = make_password(new_password)
                user.password = new_password
                user.save()
                messages.success(self.request, "Successfully updated your password.")
                return redirect(self.success_url)
            else:
                messages.error(self.request, "New passwords are not matching.")
        else:
            messages.error(self.request, "Invalid current password")
        return redirect(reverse_lazy('authentication:settings'))




class LocalizationView(BaseCrmUserView, TemplateView):
    template_name = 'crmuser/localization-details.html'


class PaymentSettingsView(BaseCrmUserView, TemplateView):
    template_name = 'crmuser/payment-settings.html'


class EmailSettingsView(BaseCrmUserView, TemplateView):
    template_name = 'crmuser/email-settings.html'


class SocialMediaLoginView(BaseCrmUserView, TemplateView):
    template_name = 'crmuser/social-settings.html'


class SocialLinksView(BaseCrmUserView, TemplateView):
    template_name = 'crmuser/social-links.html'


class SeoSettingsView(BaseCrmUserView, TemplateView):
    template_name = 'crmuser/seo-settings.html'


class OtherSettingsView(BaseCrmUserView, TemplateView):
    template_name = 'crmuser/others-settings.html'


class Error404(TemplateView):
    template_name = "error_pages/error-404.html"


class Error500(TemplateView):
    template_name = "error_pages/error-500.html"