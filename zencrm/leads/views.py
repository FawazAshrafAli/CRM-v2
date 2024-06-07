from django.http import HttpRequest, HttpResponse, Http404
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView, View
from django.shortcuts import render, redirect, get_object_or_404
from common.mixins import CrmLoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import ProtectedError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from pycountry import countries

from organizations.models import Company
from authentication.models import User
from contacts.models import Contact
from deals.models import Deal
from crm_admin.models import Customer
from .models import Lead

class BaseLeadView(CrmLoginRequiredMixin):
    model = Lead
    login_url = 'authentication:login'
    template_name = 'leads/leads.html'

    error404 = reverse_lazy('authentication:error404')
    error500 = reverse_lazy('authentication:error500')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context.update({
                "customer": get_object_or_404(Customer, organization_id = self.request.user.organization_id),
                "organizations" : Company.objects.all(),
                "users" : User.objects.filter(organization_id = self.request.user.organization_id),
                "countries": [country.name for country in countries]
            })
        except Http404:
            pass
        return context
 

class CreateLeadView(BaseLeadView, CreateView):
    template_name = 'leads/leads.html'    
    fields = "__all__"
    success_url = reverse_lazy('leads:list')
    raise_exception = True

    def post(self, request, *args, **kwargs):
        image = request.FILES.get('image')
        prefix = request.POST.get('prefix')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company = request.POST.get('company')

        try:
            company = get_object_or_404(Company, pk = company)
        except Http404:
            return HttpResponse("Invalid company")

        title = request.POST.get('title')
        lead_status = request.POST.get('lead_status')
        user_responsible = request.POST.get('user_responsible')

        try:
            user_responsible = get_object_or_404(User, pk = user_responsible)
        except Http404:
            return HttpResponse("Invalid user responsible")

        lead_rating = request.POST.get('lead_rating')
        lead_owner = request.POST.get('lead_owner')

        try:
            lead_owner = get_object_or_404(User, pk = lead_owner)
        except Http404:
            return HttpResponse("Invalid lead owner")

        email = request.POST.get('email')
        email_opted_out = request.POST.get('email_opted_out')
        phone = request.POST.get('phone')
        mobile_phone = request.POST.get('mobile_phone')
        fax = request.POST.get('fax')
        website = request.POST.get('website')
        industry = request.POST.get('industry')
        number_of_employees = request.POST.get('number_of_employees')
        lead_source = request.POST.get('lead_source')
        mailing_address = request.POST.get('mailing_address')
        mailing_city = request.POST.get('mailing_city')
        mailing_state = request.POST.get('mailing_state')
        mailing_postal_code = request.POST.get('mailing_postal_code')
        mailing_country = request.POST.get('mailing_country')
        description = request.POST.get('description')
        tag_list = request.POST.get('tag_list')
        permission = request.POST.get('permission')

        data = {
            "image": image, 
            "prefix": prefix, 
            "first_name": first_name, 
            "last_name": last_name, 
            "company": company, 
            "organization_id": self.request.user.organization_id, 
            "title": title, 
            "lead_status": lead_status, 
            "user_responsible": user_responsible, 
            "lead_rating": lead_rating, 
            "lead_owner": lead_owner, 
            "email": email, 
            "email_opted_out": email_opted_out, 
            "phone": phone, 
            "mobile_phone": mobile_phone, 
            "fax": fax, 
            "website": website, 
            "industry": industry, 
            "number_of_employees": number_of_employees, 
            "lead_source": lead_source, 
            "mailing_address": mailing_address, 
            "mailing_city": mailing_city, 
            "mailing_state": mailing_state, 
            "mailing_postal_code": mailing_postal_code, 
            "mailing_country": mailing_country, 
            "description": description, 
            "tag_list": tag_list, 
            "permission": permission, 
        }
        try:
            Lead.objects.create(**data)
            messages.success(self.request, 'Created Lead successfully.')
            return redirect(self.success_url)
        except Exception as e:
            print(e)
            return redirect(self.error500)

    def form_valid(self, form):
        messages.success(self.request, 'Created Lead successfully.')
        return super().form_valid(form)    
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Something went wrong')
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error on {field}: {error}")
        return response
    

class CloneLeadView(BaseLeadView, CreateView):        
    fields = "__all__"
    success_url = reverse_lazy('leads:list')

    def get_object(self, **kwargs):
        try:
            return get_object_or_404(Lead, pk = self.kwargs['pk'])
        except Http404:
            return redirect(reverse_lazy('authentication:error404'))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            Lead.objects.create(
                image = self.object.image,
                prefix = self.object.prefix,
                first_name = self.object.first_name,
                last_name = self.object.last_name,
                organization = self.object.company,
                title = self.object.title,
                lead_status = self.object.lead_status,
                user_responsible = self.object.user_responsible,
                lead_rating = self.object.lead_rating,
                lead_owner = self.object.lead_owner,
                email = self.object.email,
                email_opted_out = self.object.email_opted_out,
                phone = self.object.phone,
                mobile_phone = self.object.mobile_phone,
                fax = self.object.fax,
                website = self.object.website,
                industry = self.object.industry,
                number_of_employees = self.object.number_of_employees,
                lead_source = self.object.lead_source,
                mailing_address = self.object.mailing_address,
                mailing_city = self.object.mailing_city,
                mailing_state = self.object.mailing_state,
                mailing_postal_code = self.object.mailing_postal_code,
                mailing_country = self.object.mailing_country,
                description = self.object.description,
                tag_list = self.object.tag_list,
                permission = self.object.permission,            
            )
            messages.success(self.request, "Successfully cloned lead.")
            return redirect(self.get_success_url())
        except Exception as e:
            print(e)  
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Something went wrong')
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error on {field}: {error}")
        return response 

    
class ChangeLeadOwnerView(BaseLeadView, UpdateView):
    model = Lead
    fields = ["record_owner"]
    success_url = reverse_lazy('leads:list')

    def form_valid(self, form):
        messages.success(self.request, "Lead owner updation successfull.")
        return super().form_valid(form)    


class ListLeadView(BaseLeadView, ListView):
    template_name = 'leads/leads.html'
    queryset = Lead.objects.all().exclude(archived = True)
    context_object_name = 'leads'

class DetailLeadView(BaseLeadView, DetailView):
    template_name = 'leads/detail.html'
    pk_url_kwarg = 'pk'    


    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            messages.error(self.request, 'Invalid lead')
            return redirect(reverse_lazy('leads:list'))
        
    def render_to_response(self, context, **response_kwargs):
        lead = context['object']

        serialized_data = {
            "id" : lead.id,        
            "prefix" : lead.prefix,
            "first_name": lead.first_name,
            "last_name": lead.last_name,            
            "title" : lead.title,            
            "mailing_address": lead.mailing_address,
            "mailing_city": lead.mailing_city,
            "mailing_state": lead.mailing_state,
            "mailing_postal_code": lead.mailing_postal_code,
            "mailing_country": lead.mailing_country,           
            "lead_rating" : lead.lead_rating,
            "email" : lead.email,
            "email_opted_out" : lead.email_opted_out,
            "phone" : lead.phone,
            "mobile_phone" : lead.mobile_phone,
            "fax" : lead.fax,
            "website" : lead.website,
            "industry" : lead.industry,
            "number_of_employees" : lead.number_of_employees,
            "lead_source" : lead.lead_source,            
            "description" : lead.description,
            "tag_list" : lead.tag_list,
            "permission" : lead.permission,            
            "created" : lead.created.strftime("%d-%b-%y %I:%M %p"),
            "updated" : lead.updated.strftime("%d/%m/%Y")
        }

        if lead.company:
            serialized_data.update({
                "organization" : lead.company.id,
                "organization_name" : lead.company.name
            })

        if lead.lead_status:
            serialized_data["lead_status"] = lead.lead_status,

        if lead.record_owner:
            serialized_data.update({
                "lead_owner": lead.record_owner.pk,
                "lead_owner_name": lead.record_owner.full_name
                })

        if lead.image:
            serialized_data["image"] = lead.image.url

        if lead.first_name and lead.last_name:
            serialized_data["full_name"] = f"{lead.first_name} {lead.last_name}"
        elif lead.first_name:
            serialized_data["full_name"] = lead.first_name

        if lead.user_responsible:            
            serialized_data.update({
                "user_responsible" : lead.user_responsible.id,
                "user_responsible_name" : lead.user_responsible.full_name
                })

        if lead.mailing_address and lead.mailing_city and lead.mailing_state and lead.mailing_postal_code and lead.mailing_country:
            full_mailing_address = f"{lead.mailing_address}, {lead.mailing_city}, {lead.mailing_state}, {lead.mailing_postal_code}, {lead.mailing_country}."
            serialized_data['full_mailing_address'] = full_mailing_address

        return JsonResponse(serialized_data)

class UpdateLeadView(BaseLeadView, UpdateView):    
    pk_url_kwarg = 'pk'
    fields = "__all__"
    success_url = reverse_lazy('leads:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Lead updation successfull.')
        return response
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error on  field {field}: {error}")
        return  super().form_invalid(form)
    

class UpdateLeadImageView(BaseLeadView, UpdateView):    
    pk_url_kwarg = 'pk'
    fields = ["image"]
    success_url = reverse_lazy('leads:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Successfully Changed Lead Image.')
        return response    


# For updating lead status using ajax
@method_decorator(csrf_exempt, name="dispatch")
class UpdateLeadStatusView(BaseLeadView, UpdateView):
    template_name = 'leads/leads.html'
    pk_url_kwarg = 'pk'
    fields = ["lead_status"]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = {'message': 'Error'}        
        self.object.lead_status = request.POST.get('new_status')
        self.object.save()              
        data = {'message': 'Success', 'id': self.object.id}

        return JsonResponse(data)


class DeleteLeadView(BaseLeadView, View):    
    modal = Lead
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('leads:list')

    def get(self, request, *args, **kwargs):
        try:
            self.object = get_object_or_404(Lead, pk = self.kwargs['pk'])
            self.object.delete()
            messages.success(self.request, "Lead deleted successfully.")
            return redirect(self.success_url)
        except ProtectedError:
            messages.error(self.request, "Cannot delete this lead object since it has relation with objects of other models.")
            return redirect(reverse_lazy('leads:list'))
        


class ChangeLeadToContact(BaseLeadView, CreateView):
    model = Lead
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('leads:list')

    def get_object(self, **kwargs):
        try:
            return get_object_or_404(Lead, pk = self.kwargs['pk'])
        except Http404:
            return redirect(reverse_lazy('authentication:error404'))
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.contact_object = get_object_or_404(Contact, 
                              prefix = self.object.prefix, 
                              first_name = self.object.first_name, 
                              last_name = self.object.last_name,
                              organization = self.object.organization,
                              email = self.object.email,
                              phone = self.object.phone
                              )
            self.contact_object.archived = False
            self.contact_object.save()            
            self.object.delete()
            messages.success(self.request, "Change lead to contacts successfully.")
            return redirect(self.get_success_url())
        except Http404:
            try:
                Contact.objects.create(
                    image = self.object.image,
                    prefix = self.object.prefix,
                    first_name = self.object.first_name,
                    last_name = self.object.last_name,
                    organization = self.object.organization,
                    title = self.object.title,
                    email = self.object.email,
                    email_opted_out = self.object.email_opted_out,
                    phone = self.object.phone,                
                    mobile_phone = self.object.mobile_phone,                
                    fax = self.object.fax,                
                    mailing_address = self.object.mailing_address,
                    mailing_city = self.object.mailing_city,
                    mailing_state = self.object.mailing_state,
                    mailing_postal_code = self.object.mailing_postal_code,
                    mailing_country = self.object.mailing_country,                
                    description = self.object.description,
                    permission = self.object.permission,
                    tag_list = self.object.tag_list,                
                    record_owner = self.object.lead_owner,                                
                )
                self.object.delete()
                messages.success(self.request, "Change lead to contacts successfully.")
                return redirect(self.get_success_url())
            except Http404:
                pass



class ChangeLeadToDeal(BaseLeadView, CreateView):
    model = Lead
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('leads:list')

    def get_object(self, **kwargs):
        try:
            return get_object_or_404(Lead, pk = self.kwargs['pk'])
        except Http404:
            return redirect(reverse_lazy('authentication:error404'))
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()        
        try:
            get_object_or_404(Deal, 
                              prefix = self.object.prefix,
                              first_name = self.object.first_name,
                              last_name = self.object.last_name,
                              company = self.object.organization,
                              title = self.object.title,
                              email = self.object.email,
                              )            
            messages.success(self.request, "Similer deal already exists.")
            return redirect(self.get_success_url())
        except Http404:
            try:
                deal = Deal.objects.create(
                    image = self.object.image,
                    prefix = self.object.prefix,
                    company = self.object.organization,                                                                                
                    user_responsible = self.object.user_responsible,
                    description = self.object.description,
                    tag_list = self.object.tag_list,                    
                )
                deal.stage.clear()
                self.object.archived = True
                self.object.save()
                messages.success(self.request, "Changed lead to deal successfully.")
                return redirect(self.get_success_url())
            except Http404:
                pass