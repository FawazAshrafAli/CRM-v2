# Generated by Django 5.0.2 on 2024-05-16 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_admin', '0016_alter_customer_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='duration',
            field=models.FloatField(),
        ),
    ]
