# Generated by Django 5.0.2 on 2024-06-04 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0002_rename_organization_lead_company_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='organization_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
