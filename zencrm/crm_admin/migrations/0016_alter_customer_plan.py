# Generated by Django 5.0.2 on 2024-05-16 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_admin', '0015_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='plan',
            field=models.FloatField(default=0),
        ),
    ]