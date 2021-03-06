# Generated by Django 3.2.3 on 2022-01-07 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_product_availability_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart_items',
            name='returned',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Returns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('return_cost', models.IntegerField(blank=True, default=0, null=True)),
                ('return_reason', models.CharField(blank=True, max_length=50, null=True)),
                ('return_date', models.DateTimeField(auto_now=True, null=True)),
                ('return_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.cart_items')),
            ],
        ),
    ]
