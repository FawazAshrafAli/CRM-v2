from django.db import models
from organizations.models import Company
from authentication.models import User
from django.shortcuts import get_object_or_404
from django.http import Http404

class Lead(models.Model):
    # Lead Information
    image = models.ImageField(upload_to='lead_images/', blank=True, null=True)

    prefix = models.CharField(max_length=25, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, blank=True, null=True)
    organization_id = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=150, blank=False, null=False)
    lead_status = models.CharField(max_length=150, blank=False, null=False, default = 'Not Contacted')
    user_responsible = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name="user_responsible")
    lead_rating = models.IntegerField(blank=True, null=True)

    # managing
    record_owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="lead_owner", blank=True, null=True)

    # Additional Information
    email = models.EmailField(max_length=254, blank=False, null=False)
    email_opted_out = models.BooleanField(default=False, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=False, null=False)
    mobile_phone = models.CharField(max_length=20, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    website = models.CharField(max_length=150, blank=True, null=True)
    industry = models.CharField(max_length=150, blank=True, null=True)
    number_of_employees = models.CharField(max_length=50, blank=True, null=True)
    lead_source = models.CharField(max_length=150, blank=True, null=True, default="Web")

    # Address Information
    mailing_address = models.TextField(blank=False, null=False)
    mailing_city = models.CharField(max_length=50, blank=False, null=False)
    mailing_state = models.CharField(max_length=50, blank=False, null=False)
    mailing_postal_code = models.CharField(max_length=15, blank=False, null=False)
    mailing_country = models.CharField(max_length=100, blank=False, null=False)

    # Description Information
    description = models.TextField(blank=True, null=True)

    # Tag Information
    tag_list = models.CharField(max_length=150, blank=True, null=True)

    # Permissions
    permission = models.CharField(max_length=100, blank=True, null=True)

    archived = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        full_name = self.first_name
        if self.last_name:
            full_name += f" {self.last_name}"
        return full_name
    
    def __str__(self):
        return self.full_name