# Generated by Django 5.0.2 on 2024-06-03 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='people',
            new_name='host',
        ),
    ]
