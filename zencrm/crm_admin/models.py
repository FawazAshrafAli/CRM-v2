from django.db import models
import uuid

def generate_organization_id():
    return uuid.uuid4().hex[:8]

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
    duration = models.PositiveIntegerField(default=0)
    expiry_date = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=False)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
