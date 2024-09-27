# Generated by Django 4.0.6 on 2024-09-13 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0036_enddaydailyreport_delivery_grandtotal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='background_image',
            field=models.ImageField(blank=True, null=True, upload_to='organization/images'),
        ),
        migrations.AddField(
            model_name='organization',
            name='review_points',
            field=models.FloatField(default=0.0),
        ),
    ]
