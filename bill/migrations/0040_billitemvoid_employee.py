# Generated by Django 4.0.6 on 2024-10-22 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0039_order_completed_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='billitemvoid',
            name='employee',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]