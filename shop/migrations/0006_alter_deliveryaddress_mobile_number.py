# Generated by Django 3.2.3 on 2021-11-17 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20211117_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryaddress',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
