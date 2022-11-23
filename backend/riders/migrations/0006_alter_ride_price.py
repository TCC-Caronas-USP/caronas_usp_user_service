# Generated by Django 4.1.3 on 2022-11-23 01:06

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riders', '0005_ride_notification_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]
