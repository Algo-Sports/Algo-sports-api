# Generated by Django 3.1.3 on 2020-12-12 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codes', '0009_programminglanguage_template_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programminglanguage',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Programming language'),
        ),
    ]
