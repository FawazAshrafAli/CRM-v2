from django.db import models
from authentication.models import User
from contacts.models import Contact
from leads.models import Lead
from deals.models import Deal

class Activity(models.Model):
    activity = models.CharField(max_length=150, blank=False, null=False)
    starting_date = models.DateField()
    starting_time = models.TimeField()
    ending_date = models.DateField()
    ending_time = models.TimeField()

    # availability = models.CharField(max_length=150, blank=True, null=True, default="Busy")
    notes = models.TextField(blank=True, null=True)

    user_responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    guest_type = models.CharField(max_length=150, blank=True, null=True)
    host = models.CharField(max_length=250, blank=False, null=False)
    contact_guest = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True)
    lead_guest = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True)
    deal_guest = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True, blank=True)
    # organization = models.CharField(max_length=150, blank=True, null=True)

    # meeting_follow_up_action = models.CharField(max_length=150, blank=True, null=True)

    # Meeing & Lunch/Meal
    title = models.CharField(max_length=150, blank=True, null=True)
    purpose = models.CharField(max_length=150, blank=True, null=True)
    location = models.CharField(max_length=150, blank=True, null=True)
    contact_guests = models.ManyToManyField(Contact, related_name="contact_guests")
    lead_guests = models.ManyToManyField(Lead, related_name="lead_guests")
    deal_guests = models.ManyToManyField(Deal, related_name="deal_guests")

    # # Lunch/Meal
    additional_information = models.TextField(blank=True, null=True)

    # # Flagged
    # Title = models.CharField(max_length=150, blank=True, null=True)    
    # flagged_datetime = models.DateTimeField(null=True, blank=True)
    # reason_for_flagging = models.TextField(blank=True, null=True)
    # flag_type = models.CharField(max_length=150, blank=True, null=True)    #e.g., priority level, status    
    # flagged_user = models.CharField(max_length=150, blank=True, null=True)    
    # due_date = models.DateField(null=True, blank=True)
    # Status = models.CharField(max_length=150, blank=True, null=True)     # open/completed/dismissed

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def starting_datetime(self):
        if self.starting_date and self.starting_time:
            return f"{self.starting_date.strftime("%d-%b-%Y")} {self.starting_time.strftime("%I:%M %p")}"
        return None
    
    @property
    def ending_datetime(self):
        if self.ending_date and self.ending_time:
            return f"{self.ending_date.strftime("%d-%b-%Y")} {self.ending_time.strftime("%I:%M %p")}"
        return None

    @property
    def guest(self):
        guests = [self.contact_guest, self.lead_guest, self.deal_guest]
        for guest in guests:
            if guest:
                return guest
        guests_list = [self.contact_guests, self.lead_guests, self.deal_guests]
        for guests in guests_list:
            if guests.all().count() == 1:
                return guests.all().first()
        return None
    
    @property
    def guests(self):
        guests_list = [self.contact_guests, self.lead_guests, self.deal_guests]
        for guests in guests_list:
            if guests.all().count() > 1:
                return guests.all()
        return None
    
    @property
    def guests_team(self):
        # if self.guests:
        #     guests = self.guests
        #     if guests.count() > 1:
        #         team =  f"{guests[0].full_name} + {guests.count() - 1} more"
        #     else:
        #         team = guests[0].full_name
        #     return team
        # return None
        if self.guests:
            guests = self.guests
            not_none_list = []
            if guests.count() > 0:
                for guest in guests:
                    if guest.full_name is not None:
                        not_none_list.append(guest)
                    else:
                        continue
            list_length = len(not_none_list)
            if list_length > 1:
                return f"{not_none_list[0].full_name} + {list_length - 1} more"
            elif list_length > 0:
                return not_none_list[0].full_name
        return None
    
    @property
    def guests_team_email(self):
        if self.guests:
            guests = self.guests
            not_none_list = []
            if guests.count() > 0:
                for guest in guests:
                    if guest.email is not None:
                        not_none_list.append(guest)
                    else:
                        continue
            list_length = len(not_none_list)
            if list_length > 1:
                return f"{not_none_list[0].email} + {list_length - 1} more"
            elif list_length > 0:
                return not_none_list[0].email
        return None
    
    @property
    def guests_team_phone(self):
        if self.guests:
            guests = self.guests
            not_none_list = []
            if guests.count() > 0:
                for guest in guests:
                    if guest.phone is not None:
                        not_none_list.append(guest)
                    else:
                        continue
            list_length = len(not_none_list)
            if list_length > 1:
                return f"{not_none_list[0].phone} + {list_length - 1} more"
            elif list_length > 0:
                return not_none_list[0].phone
        return None
    
    @property
    def target_modal(self):
        if self.guest_type:
            return f"#{self.guest_type.lower()}-modal"
        return "#"
    
    @property
    def js_function(self):
        if self.guest_type:
            return f"load{self.guest_type}Details"
        return ""

    def __str__(self):
        if self.guest:
            return f"{self.activity} - {self.guest}"
        elif self.guests_team:
            return f"{self.activity} - {self.guests_team}"
        else:
            return self.activity