# Generated by Django 4.0.6 on 2024-09-30 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_itemreconcilationapiitem_physical_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='print_display',
            field=models.CharField(blank=True, choices=[('KITCHEN', 'KITCHEN'), ('FOOD', 'FOOD')], max_length=255, null=True),
        ),
    ]
