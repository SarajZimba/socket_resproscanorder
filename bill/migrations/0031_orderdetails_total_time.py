# Generated by Django 4.0.6 on 2024-09-30 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0030_orderdetails_completed_from'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='total_time',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
