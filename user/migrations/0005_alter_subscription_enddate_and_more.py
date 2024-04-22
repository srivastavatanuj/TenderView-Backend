# Generated by Django 5.0.4 on 2024-04-17 21:10

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_subscription_issubscribed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='endDate',
            field=models.DateField(default=datetime.date(2024, 4, 27)),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='startDate',
            field=models.DateField(default=datetime.date(2024, 4, 17)),
        ),
        migrations.AlterField(
            model_name='user',
            name='companyName',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[a-zA-Z0-9 ]{5,100}$', message='Company name not valid')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=100),
        ),
    ]
