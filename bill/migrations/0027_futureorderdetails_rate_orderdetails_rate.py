# Generated by Django 4.0.6 on 2024-09-26 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0026_futureorder_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='futureorderdetails',
            name='rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
