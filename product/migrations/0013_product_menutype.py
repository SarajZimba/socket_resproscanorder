# Generated by Django 4.0.6 on 2024-09-13 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0007_menu_resproproduct'),
        ('product', '0012_product_delete_check_product_is_veg_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='menutype',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.menutype'),
        ),
    ]