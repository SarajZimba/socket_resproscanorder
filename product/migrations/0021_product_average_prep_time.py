# Generated by Django 4.0.6 on 2024-10-01 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0020_product_print_display'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='average_prep_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]