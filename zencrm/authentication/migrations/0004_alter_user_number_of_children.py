# Generated by Django 5.0.2 on 2024-04-25 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_user_number_of_children'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='number_of_children',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
