# Generated by Django 4.0.6 on 2024-09-16 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_branchstocktracking_closing_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemreconcilationapiitem',
            name='physical',
        ),
        migrations.RemoveField(
            model_name='itemreconcilationapiitem',
            name='returned',
        ),
        migrations.RemoveField(
            model_name='itemreconcilationapiitem',
            name='wastage',
        ),
    ]
