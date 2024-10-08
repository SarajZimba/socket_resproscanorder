# Generated by Django 4.0.6 on 2024-10-01 04:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0020_product_print_display'),
        ('bill', '0031_orderdetails_total_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='tblOrderTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('product_quantity', models.PositiveBigIntegerField(default=1)),
                ('kotID', models.CharField(blank=True, max_length=255, null=True)),
                ('botID', models.CharField(blank=True, max_length=255, null=True)),
                ('modification', models.CharField(blank=True, max_length=255, null=True)),
                ('ordertime', models.CharField(blank=True, max_length=255, null=True)),
                ('employee', models.CharField(blank=True, max_length=255, null=True)),
                ('rate', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('done', models.BooleanField(default=False)),
                ('seen', models.BooleanField(default=False)),
                ('completed_time', models.CharField(blank=True, max_length=255, null=True)),
                ('completed_from', models.CharField(blank=True, max_length=255, null=True)),
                ('total_time', models.CharField(blank=True, max_length=255, null=True)),
                ('average_prep_time', models.CharField(blank=True, max_length=255, null=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bill.order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
