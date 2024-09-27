# Generated by Django 4.0.6 on 2023-10-03 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0017_alter_cashdrop_datetime'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='table',
            options={},
        ),
        migrations.AddField(
            model_name='branch',
            name='branch_image',
            field=models.ImageField(blank=True, null=True, upload_to='branch_images/'),
        ),
        migrations.AddField(
            model_name='cashdrop',
            name='addCash',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='cashdrop',
            name='narration',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='cashdrop',
            name='terminal',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cashdrop',
            name='branch_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.branch'),
        ),
        migrations.AlterField(
            model_name='cashdrop',
            name='expense',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='cashdrop',
            name='remaining_balance',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterUniqueTogether(
            name='table',
            unique_together={('terminal', 'table_number')},
        ),
        migrations.CreateModel(
            name='Table_Layout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('dx', models.FloatField(default=0.0)),
                ('dy', models.FloatField(default=0.0)),
                ('width', models.FloatField(default=0.0)),
                ('height', models.FloatField(default=0.0)),
                ('orientation', models.CharField(blank=True, max_length=200, null=True)),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='organization.branch')),
                ('table_id', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.table')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
