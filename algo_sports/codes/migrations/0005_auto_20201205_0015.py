# Generated by Django 3.1.3 on 2020-12-05 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codes', '0004_auto_20201203_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='programminglanguage',
            name='compile_cmd',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='programminglanguage',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='programminglanguage',
            name='run_cmd',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
