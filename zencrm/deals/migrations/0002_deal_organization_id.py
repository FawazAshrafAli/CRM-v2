# Generated by Django 5.0.2 on 2024-06-03 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='organization_id',
            field=models.CharField(default=None, max_length=20),
            preserve_default=False,
        ),
    ]
