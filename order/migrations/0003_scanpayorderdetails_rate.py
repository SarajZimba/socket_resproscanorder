# Generated by Django 4.0.6 on 2024-09-26 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_scanpayorder_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='scanpayorderdetails',
            name='rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
