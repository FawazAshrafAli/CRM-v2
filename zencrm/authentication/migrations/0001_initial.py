# Generated by Django 5.0.2 on 2024-04-25 12:57

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrmUserEducation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crm_user_id', models.CharField(max_length=50)),
                ('institution', models.CharField(max_length=150)),
                ('course', models.CharField(max_length=150)),
                ('started_year', models.CharField(max_length=50)),
                ('completed_year', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'ordering': ['started_year'],
            },
        ),
        migrations.CreateModel(
            name='CrmUserExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crm_user_id', models.CharField(max_length=50)),
                ('designation', models.CharField(max_length=150)),
                ('company', models.CharField(max_length=150)),
                ('started_month_and_year', models.CharField(max_length=50)),
                ('completed_month_and_year', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CrmUserFamilyInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crm_user_id', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=150)),
                ('relationship', models.CharField(max_length=150)),
                ('date_of_birth', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('image', models.ImageField(blank=True, null=True, upload_to='crm_user_images/')),
                ('organization', models.CharField(blank=True, max_length=150, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=16, null=True, unique=True)),
                ('birthday', models.CharField(blank=True, max_length=150, null=True)),
                ('address', models.CharField(blank=True, max_length=150, null=True)),
                ('address_city', models.CharField(blank=True, max_length=150, null=True)),
                ('address_state', models.CharField(blank=True, max_length=150, null=True)),
                ('address_postal_code', models.CharField(blank=True, max_length=150, null=True)),
                ('address_country', models.CharField(blank=True, max_length=150, null=True)),
                ('gender', models.CharField(blank=True, max_length=50, null=True)),
                ('team', models.CharField(blank=True, max_length=150, null=True)),
                ('passport_number', models.CharField(blank=True, max_length=25, null=True, unique=True)),
                ('passport_expiry_date', models.CharField(blank=True, max_length=50, null=True)),
                ('tel', models.CharField(blank=True, max_length=16, null=True, unique=True)),
                ('nationality', models.CharField(blank=True, max_length=100, null=True)),
                ('religion', models.CharField(blank=True, max_length=100, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=75, null=True)),
                ('employment_of_spouse', models.CharField(blank=True, max_length=150, null=True)),
                ('number_of_children', models.PositiveIntegerField(blank=True, null=True)),
                ('primary_contact_name', models.CharField(blank=True, max_length=100, null=True)),
                ('primary_contact_relationship', models.CharField(blank=True, max_length=100, null=True)),
                ('primary_contact_phone1', models.CharField(blank=True, max_length=100, null=True)),
                ('primary_contact_phone2', models.CharField(blank=True, max_length=100, null=True)),
                ('secondary_contact_name', models.CharField(blank=True, max_length=100, null=True)),
                ('secondary_contact_relationship', models.CharField(blank=True, max_length=100, null=True)),
                ('secondary_contact_phone1', models.CharField(blank=True, max_length=100, null=True)),
                ('secondary_contact_phone2', models.CharField(blank=True, max_length=100, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=150, null=True)),
                ('bank_account_number', models.CharField(blank=True, max_length=25, null=True)),
                ('ifsc_code', models.CharField(blank=True, max_length=25, null=True)),
                ('pan_number', models.CharField(blank=True, max_length=25, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('reports_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('education_info', models.ManyToManyField(to='authentication.crmusereducation')),
                ('experience', models.ManyToManyField(to='authentication.crmuserexperience')),
                ('family_info', models.ManyToManyField(to='authentication.crmuserfamilyinformation')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
