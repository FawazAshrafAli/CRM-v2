# Generated by Django 5.0.2 on 2024-05-13 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm_admin', '0013_remove_customer_expiry_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='duration',
            new_name='plan',
        ),
    ]
