# Generated by Django 4.0.6 on 2024-10-01 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0033_tblordertracker_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblordertracker',
            name='prep_time_difference',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
