# Generated by Django 4.0.6 on 2024-06-03 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0032_alter_mailrecipient_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='auto_end_day',
            field=models.BooleanField(default=True),
        ),
    ]
