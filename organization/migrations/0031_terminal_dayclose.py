# Generated by Django 4.0.6 on 2024-05-14 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0030_remove_terminal_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='terminal',
            name='dayclose',
            field=models.BooleanField(default=False),
        ),
    ]
