# Generated by Django 5.0.4 on 2024-04-14 10:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(db_index=True, max_length=10, unique=True, validators=[django.core.validators.RegexValidator('^[0-9]{10}$', message='Phone number must be 10 digits')]),
        ),
    ]