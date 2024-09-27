# Generated by Django 4.0.6 on 2024-09-13 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_productpoints_customerproductpointstrack'),
        ('menu', '0006_remove_menu_resproproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='resproproduct',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
    ]
