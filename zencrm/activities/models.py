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

    availability = models.CharField(max_length=150, blank=True, null=True, default="Busy")
    notes = models.TextField(blank=True, null=True)

    user_responsible = models.ForeignKey(User, on_delete=models.CASCADE)
    guest_type = models.CharField(max_length=150, blank=True, null=True)
    host = models.CharField(max_length=250, blank=False, null=False)
    contact_guest = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True)
    lead_guest = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True)
    deal_guest = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True, blank=True)
    organization = models.CharField(max_length=150, blank=True, null=True)

    # meeting_follow_up_action = models.CharField(max_length=150, blank=True, null=True)

    # # Meeting
    meeting_title = models.CharField(max_length=150, blank=True, null=True)
    meeting_location = models.CharField(max_length=150, blank=True, null=True)
    meeting_purpose = models.CharField(max_length=150, blank=True, null=True)
    contact_guest = models.ManyToManyField(Contact)
    lead_guest = models.ManyToManyField(Lead)
    deal_guest = models.ManyToManyField(Deal)

    # # Lunch/Meal
    # meal_organizer = models.CharField(max_length=150, blank=True, null=True)
    # mead_title = models.CharField(max_length=150, blank=True, null=True)    
    # meal_location = models.CharField(max_length=150, blank=True, null=True)    
    # meal_attendees = models.JSONField(blank=True, null=True, default=list)
    # meal_menu = models.JSONField(blank=True, null=True, default=list)
    # meal_purpose = models.CharField(max_length=150, blank=True, null=True)    
    # meal_special_requirements = models.TextField(blank=True, null=True)

    # # Flagged
    # Title = models.CharField(max_length=150, blank=True, null=True)    
    # flagged_datetime = models.DateTimeField(null=True, blank=True)
    # reason_for_flagging = models.TextField(blank=True, null=True)
    # flag_type = models.CharField(max_length=150, blank=True, null=True)    #e.g., priority level, status    
    # flagged_user = models.CharField(max_length=150, blank=True, null=True)    
    # due_date = models.DateField(null=True, blank=True)
    # Status = models.CharField(max_length=150, blank=True, null=True)     # open/completed/dismissed

