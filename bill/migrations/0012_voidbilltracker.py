# Generated by Django 4.0.6 on 2024-05-07 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0011_order_terminal_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoidBillTracker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('prev_bill', models.CharField(blank=True, max_length=255, null=True)),
                ('new_bill', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]