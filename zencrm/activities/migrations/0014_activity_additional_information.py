# Generated by Django 5.0.2 on 2024-06-06 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0013_activity_created_activity_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='additional_information',
            field=models.TextField(blank=True, null=True),
        ),
    ]
