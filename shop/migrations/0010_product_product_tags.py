# Generated by Django 3.2.3 on 2022-02-08 00:13

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0004_alter_taggeditem_content_type_alter_taggeditem_tag'),
        ('shop', '0009_auto_20220107_0754'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]