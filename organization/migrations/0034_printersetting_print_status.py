# Generated by Django 4.0.6 on 2024-06-05 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0033_organization_auto_end_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='printersetting',
            name='print_status',
            field=models.BooleanField(default=False),
        ),
    ]
