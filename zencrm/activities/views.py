from django.shortcuts import redirect, get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from common.mixins import CrmLoginRequiredMixin
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import Http404, JsonResponse, HttpResponse
from django.urls import reverse_lazy
import datetime
from datetime import datetime as dt
import traceback

from crm_admin.models import Customer
from .models import Activity
from authentication.models import User
from contacts.models import Contact
from leads.models import Lead
from deals.models import Deal

@method_decorator(never_cache, name='dispatch')
class BaseActivityView(CrmLoginRequiredMixin):
    login_url = 'authentication:login'
    model = Activity
    template_name = "activities/activities.html"

    error404 = reverse_lazy('authentication:error404')
    error500 = reverse_lazy('authentication:error500')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['customer'] = get_object_or_404(Customer, organization_id = self.request.user.organization_id)
        except Http404:
            pass

        models = [User, Contact, Lead, Deal]
        for model in models:
            try:
                model_name = model.__name__.lower() + "s"
                query_set = get_list_or_404(model, organization_id = self.request.user.organization_id)
                context[model_name] = query_set
            except Http404:
                pass

        return context


class ActivityListView(BaseActivityView, ListView):
    model = Activity
    queryset = Activity.objects.all()
    context_object_name = 'activities'


class CreateActivityView(BaseActivityView, CreateView):
    modal = Activity
    fields = "__all__"
    success_url = reverse_lazy('activities:list')

    def manage_call(self, request, guest_type, data):
        if guest_type == "Contact":
            contact_guest = request.POST.get('contact')
            try:
                contact_guest = get_object_or_404(Contact, pk = contact_guest)
                data['contact_guest'] = contact_guest
            except:
                return HttpResponse("Invalid contact")
        elif guest_type == "Lead":
            lead_guest = request.POST.get('lead')
            try:
                lead_guest = get_object_or_404(Lead, pk = lead_guest)
                data['lead_guest'] = lead_guest
            except:
                return HttpResponse("Invalid lead")
        elif guest_type == "Deal":
            deal_guest = request.POST.get('deal')
            try:
                deal_guest = get_object_or_404(Deal, pk = deal_guest)
                data['deal_guest'] = deal_guest
            except:
                return HttpResponse("Invalid deal")
        else:
            return HttpResponse("Guest is not provided")
        
        return data

    def manage_meeting_and_meal(self, request, guest_type, data):        

        title = request.POST.get('title')
        purpose = request.POST.get('purpose')
        location = request.POST.get('location')

        data.update({
            "title": title,
            "purpose": purpose,
            "location": location
        })

        guests = None
        if guest_type == "Contact":
            contact_guest = request.POST.get('contact')
            contact_guests = request.POST.getlist('contacts')

            if contact_guest:
                try:
                    contact_guest = get_object_or_404(Contact, pk = contact_guest)
                    data['contact_guest'] = contact_guest
                except:
                    return HttpResponse("Invalid contact")
                
            elif contact_guests:
                guests = contact_guests
            
        elif guest_type == "Lead":
            lead_guest = request.POST.get('lead')
            lead_guests = request.POST.getlist('leads')

            if lead_guest:
                try:
                    lead_guest = get_object_or_404(Lead, pk = lead_guest)
                    data['lead_guest'] = lead_guest
                except:
                    return HttpResponse("Invalid lead")
                
            elif lead_guests:
                guests =  lead_guests                    
            
        elif guest_type == "Deal":
            deal_guest = request.POST.get('deal')
            deal_guests = request.POST.getlist('deals')

            if deal_guest:
                try:
                    deal_guest = get_object_or_404(Deal, pk = deal_guest)
                    data['deal_guest'] = deal_guest
                except:
                    return HttpResponse("Invalid deal")
                
            elif deal_guests:
                guests =  deal_guests            
            
        else:
            messages.warning(request, "Cannot create activity without providing atleast a single guest.")
            return redirect(reverse_lazy('activities:list'))

        return data, guests or None
    
    def manage_meal(self, request, data):
        additional_information =request.POST.get("additional_information")
        data["additional_information"] = additional_information
        return data

    def set_many_to_many(self, activity_object, guest_type, *guests):
        guest_count = len(*guests)
        guests_list = list(*guests)
        if guest_count > 0:
            if guest_type == "Contact":
                try:
                    if guest_count > 1:
                        activity_object.contact_guests.set(*guests)                        
                    else:
                        try:
                            contact = get_object_or_404(Contact, pk = guests_list[0])
                            activity_object.contact_guest = contact
                        except Http404:
                            pass

                    activity_object.save()
                except Exception as e:
                    print(f"Exception: {e}")
            
            elif guest_type == "Lead":
                try:
                    if guest_count > 1:
                        activity_object.lead_guests.set(*guests)
                    else:
                        try:
                            lead = get_object_or_404(Lead, pk = guests_list[0])
                            activity_object.lead_guest = lead
                        except Http404:
                            pass

                    activity_object.save()
                except Exception as e:
                    print(f"Exception: {e}")

            elif guest_type == "Deal":
                try:
                    if guest_count > 1:
                        activity_object.deal_guests.set(*guests)
                    else:
                        try:
                            deal = get_object_or_404(Deal, pk = guests_list[0])
                            activity_object.deal_guest = deal
                        except Http404:
                            pass

                    activity_object.save()
                except Exception as e:
                    print(f"Exception: {e}")
        else:
            pass

    def post(self, request, *args, **kwargs):
        data = {}

        activity = request.POST.get("activity")
        starting_time = request.POST.get("starting_time")
        ending_time = request.POST.get("ending_time")
        notes = request.POST.get("notes")
        host = request.POST.get("host")
        guest_type = request.POST.get("guest_type")
        user_responsible = request.POST.get("user_responsible")

        try:
            user_responsible = get_object_or_404(User, pk = user_responsible)
        except Http404:
            messages.error(request, "Please provide user responsible and try again.")
            return redirect(reverse_lazy('activities:list'))

        starting_date = request.POST.get("starting_date")
        ending_date = request.POST.get("ending_date")

        starting_date = dt.strptime(starting_date, "%d/%m/%Y")
        ending_date = dt.strptime(ending_date, "%d/%m/%Y")

        data = {
            "activity": activity, 
            "starting_date": starting_date, 
            "starting_time": starting_time,
            "ending_date": ending_date, 
            "ending_time": ending_time, 
            "notes": notes, 
            "guest_type": guest_type,
            "host": host, 
            "user_responsible": user_responsible
        }

        if activity == "Call":
            self.manage_call(request, guest_type, data)
        
        elif activity == "Meeting" or activity == "Meal":            
            data, guests = self.manage_meeting_and_meal(request, guest_type, data)
            if activity == "Meal":
                data = self.manage_meal(request, data)
        
        try:
            activity_object = Activity.objects.create(**data)

            if guests and activity == "Meeting" or activity == "Meal":                
                self.set_many_to_many(activity_object, guest_type, guests)
            
            if activity_object.guest is None and activity_object.guests is None:
                activity_object.delete()
                messages.warning(self.request, "Cannot create activity without providing atleast a single guest.")
                return redirect(reverse_lazy('activities:list'))
            
            messages.success(self.request, "Activity creation successfull.")
            return redirect(self.success_url)
        except Exception as e:
            print("Exception occurred:", e)
            traceback.print_exc()
            return redirect(self.error500)

    def form_valid(self, form):
        messages.success(self.request, "Activity creation successfull.")
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error on field {field}: {error}")
        return redirect(self.error500)
    

class FetchGuestView(BaseActivityView, View):
    model = Activity

    def get(self, request, *args, **kwargs):
        guest_type = request.GET.get('guest_type')

        guest_data = ''
        if guest_type == "Contact":
            guest_data = Contact.objects.filter(organization_id = self.request.user.organization_id)
        elif guest_type == 'Lead':
            guest_data = Lead.objects.filter(organization_id = self.request.user.organization_id)
        elif guest_type == "Deal":
            guest_data = Deal.objects.filter(organization_id = self.request.user.organization_id)
        
        if guest_data:
            return JsonResponse({'guest_data': list(guest_data.values())}, safe=True)
        else:
            return JsonResponse({'message': 'No data found.'})
        

class ActivityDetailView(BaseActivityView, DetailView):
    model = Activity

    def render_to_response(self, context):
        activity = context['object']

        serialized_data = {}

        for field in activity._meta.fields:
            field_name = field.name
            field_value = getattr(activity, field_name)

            if field_value:
                if field_name == "user_responsible":
                    serialized_data[field_name] = field_value.full_name                    

                elif field_name in ["contact_guest", "lead_guest", "deal_guest"]:        
                    serialized_data['guest'] = field_value.full_name
                    serialized_data['email'] = field_value.email
                    serialized_data['phone'] = field_value.phone
                    if field_value.record_owner:
                        serialized_data['owner'] = field_value.record_owner.full_name                
                
                elif isinstance(field_value, datetime.datetime) or isinstance(field_value, datetime.time):
                    pass

                else:
                    serialized_data[field_name] = field_value
            
        serialized_data['starting_date'] = activity.starting_date.strftime("%d/%m/%y")
        serialized_data['starting_time'] = activity.starting_time
        serialized_data['starting_datetime'] = activity.starting_datetime

        serialized_data['ending_date'] = activity.ending_date.strftime("%d/%m/%y")
        serialized_data['ending_time'] = activity.ending_time
        serialized_data['ending_datetime'] = activity.ending_datetime

        if activity.guests:
            if len(activity.guests) > 1:
                guests_list = []
                for guest in activity.guests:
                    guests_list.append(guest.full_name)
                serialized_data['guests'] = guests_list
            else:
                serialized_data['guest'] = activity.guests[0].full_name
                
            serialized_data['phone'] = activity.guests_team_phone
            serialized_data['email'] = activity.guests_team_email

        return JsonResponse(serialized_data, safe=False)

