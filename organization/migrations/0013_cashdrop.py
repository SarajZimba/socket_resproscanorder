# Generated by Django 4.0.6 on 2023-09-13 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0012_alter_enddaydailyreport_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashDrop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.CharField(max_length=200)),
                ('balance', models.FloatField(default=0.0)),
                ('datetime', models.DateTimeField()),
                ('cashdrop_amount', models.FloatField(default=0.0)),
                ('employee', models.CharField(max_length=100)),
            ],
        ),
    ]
