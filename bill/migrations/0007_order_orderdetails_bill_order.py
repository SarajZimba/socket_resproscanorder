# Generated by Django 4.0.6 on 2024-04-22 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_recipieitemsale_productrecipie'),
        ('organization', '0021_cashdrop_latest_balance'),
        ('bill', '0006_billitem_branch'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('table_no', models.IntegerField(blank=True, null=True)),
                ('date', models.CharField(blank=True, max_length=100, null=True)),
                ('sale_id', models.IntegerField(blank=True, null=True)),
                ('start_datetime', models.CharField(blank=True, max_length=255, null=True)),
                ('is_completed', models.BooleanField(blank=True, default=False, null=True)),
                ('no_of_guest', models.IntegerField(blank=True, null=True)),
                ('employee', models.CharField(blank=True, max_length=255, null=True)),
                ('order_type', models.CharField(blank=True, max_length=255, null=True)),
                ('is_saved', models.BooleanField(blank=True, default=True, null=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.branch')),
                ('terminal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.terminal')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderDetails',
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
                ('ordertime', models.CharField(blank=True, max_length=255, null=True)),
                ('employee', models.CharField(blank=True, max_length=255, null=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bill.order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='bill',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bill.order'),
        ),
    ]
