# Generated by Django 3.2.3 on 2021-12-19 18:06

from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_deliveryaddress_mobile_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='icon_image',
            field=models.ImageField(blank=True, null=True, upload_to=shop.models.get_icon_upload_path),
        ),
    ]
