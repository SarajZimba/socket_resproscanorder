# Generated by Django 4.0.6 on 2024-10-22 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0038_futureorder_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='completed_time',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]