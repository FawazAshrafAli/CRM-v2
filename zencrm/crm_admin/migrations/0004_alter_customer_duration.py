# Generated by Django 5.0.2 on 2024-04-26 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_admin', '0003_customer_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='duration',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
