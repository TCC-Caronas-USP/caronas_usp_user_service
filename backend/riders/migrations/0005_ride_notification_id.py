# Generated by Django 4.1.3 on 2022-11-19 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riders', '0004_rename_ano_rider_ingress_year_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='notification_id',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]