# Generated by Django 4.0.6 on 2024-05-10 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0016_billitemvoid_count_billitemvoid_isbefore_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='billitemvoid',
            name='reason',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]