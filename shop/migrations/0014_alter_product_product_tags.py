# Generated by Django 3.2.3 on 2022-02-13 03:57

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
        ('shop', '0013_product_on_sale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]