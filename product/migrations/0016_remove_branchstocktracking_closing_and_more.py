# Generated by Django 4.0.6 on 2024-09-16 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_recipieitemsale_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branchstocktracking',
            name='closing',
        ),
        migrations.RemoveField(
            model_name='branchstocktracking',
            name='discrepancy',
        ),
        migrations.RemoveField(
            model_name='branchstocktracking',
            name='opening',
        ),
        migrations.RemoveField(
            model_name='branchstocktracking',
            name='physical',
        ),
        migrations.RemoveField(
            model_name='branchstocktracking',
            name='received',
        ),
        migrations.RemoveField(
            model_name='branchstocktracking',
            name='returned',
        ),
        migrations.RemoveField(
            model_name='branchstocktracking',
            name='sold',
        ),
        migrations.RemoveField(
            model_name='branchstocktracking',
            name='wastage',
        ),
    ]
