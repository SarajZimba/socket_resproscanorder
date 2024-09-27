# Generated by Django 4.0.6 on 2023-05-26 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_enddaydailyreport_branch_enddaydailyreport_terminal'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailRecipient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
    ]
