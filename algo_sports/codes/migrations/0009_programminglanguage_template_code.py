# Generated by Django 3.1.3 on 2020-12-11 23:26

import algo_sports.codes.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codes', '0008_auto_20201207_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='programminglanguage',
            name='template_code',
            field=models.JSONField(default=algo_sports.codes.models.make_template_code),
        ),
    ]
