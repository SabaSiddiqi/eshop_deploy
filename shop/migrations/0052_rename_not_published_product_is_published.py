# Generated by Django 3.2.3 on 2021-06-19 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0051_auto_20210619_1543'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='not_published',
            new_name='is_published',
        ),
    ]