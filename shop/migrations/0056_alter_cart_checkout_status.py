# Generated by Django 3.2.3 on 2021-10-11 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0055_auto_20210711_2349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='checkout_status',
            field=models.BooleanField(default=False),
        ),
    ]