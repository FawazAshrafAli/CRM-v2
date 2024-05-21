from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

def generate_organization_id():
    return (uuid.uuid4().hex[:8]).upper()

class Customer(models.Model):
    name = models.CharField(max_length=150)
    organization = models.CharField(max_length=150, unique=True)
    organization_id = models.CharField(max_length=10, default=generate_organization_id, unique=True)
    logo = models.ImageField(upload_to="customer_logo/", blank=True, null=True)
    type_of_organization = models.CharField(max_length=150)
    no_of_users = models.PositiveIntegerField(default=0)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    amount = models.CharField(max_length=20, blank=True, null=True)
    plan = models.FloatField(default=0)
    active = models.BooleanField(default=True)

    website_name = models.CharField(max_length=150, blank=True, null=True)
    favicon = models.ImageField(upload_to="customer_favicon/", blank=True, null=True)    
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def expiry_date(self):
        expiry_date = self.created + timedelta(days=365*self.plan)
        if expiry_date < timezone.now():
            self.active = False
            self.save()
        return expiry_date
    

class Plan(models.Model):
    name = models.CharField(max_length=150, unique=True)
    duration = models.FloatField(unique=True)    #duration in year

    def __str__(self):
        return self.name

