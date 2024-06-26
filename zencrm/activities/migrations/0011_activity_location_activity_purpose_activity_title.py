# Generated by Django 5.0.2 on 2024-06-05 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0010_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='location',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='purpose',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='title',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
