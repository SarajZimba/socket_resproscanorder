# Generated by Django 4.0.6 on 2023-05-31 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_itemreconcilationapiitem_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemreconcilationapiitem',
            name='terminal',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
