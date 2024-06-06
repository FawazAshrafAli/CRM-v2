# Generated by Django 5.0.2 on 2024-06-05 14:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0012_activity_contact_guests_activity_deal_guests_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 6, 5, 14, 27, 26, 148904)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
