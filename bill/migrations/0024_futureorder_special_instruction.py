# Generated by Django 4.0.6 on 2024-07-03 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0023_futureorder_converted_to_normal'),
    ]

    operations = [
        migrations.AddField(
            model_name='futureorder',
            name='special_instruction',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
