# Generated by Django 3.1.3 on 2020-12-15 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_auto_20201120_1843'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['id']},
        ),
    ]