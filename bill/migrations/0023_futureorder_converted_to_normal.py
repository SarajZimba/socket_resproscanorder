# Generated by Django 4.0.6 on 2024-07-03 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0022_futureorder_futureorderdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='futureorder',
            name='converted_to_normal',
            field=models.BooleanField(default=False),
        ),
    ]
