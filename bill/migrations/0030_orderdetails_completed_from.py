# Generated by Django 4.0.6 on 2024-09-30 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0029_orderdetails_completed_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='completed_from',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
