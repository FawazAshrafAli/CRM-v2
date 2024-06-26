# Generated by Django 5.0.2 on 2024-06-05 09:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0007_rename_deal_or_lead_activity_guest_type'),
        ('contacts', '0007_alter_contact_organization_id_alter_contact_phone'),
        ('deals', '0003_alter_deal_organization_id'),
        ('leads', '0004_alter_lead_email_opted_out'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='contact_guest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contacts.contact'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='deal_guest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='deals.deal'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='lead_guest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='leads.lead'),
        ),
    ]
