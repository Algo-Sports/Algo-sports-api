# Generated by Django 3.0.10 on 2020-11-12 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AddField(
            model_name='user',
            name='language',
            field=models.CharField(blank=True, max_length=30, verbose_name='Language of User'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_id',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
