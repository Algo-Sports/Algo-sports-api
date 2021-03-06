# Generated by Django 3.1.3 on 2020-12-13 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0007_auto_20201213_1433'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('codes', '0010_auto_20201212_0051'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercode',
            old_name='gamematchs',
            new_name='gamematches',
        ),
        migrations.RenameField(
            model_name='usercode',
            old_name='gameroom',
            new_name='gamerooms',
        ),
        migrations.AlterField(
            model_name='judgementcode',
            name='gameversion_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='judgementcodes', to='games.gameversion', verbose_name='Game version'),
        ),
        migrations.AlterField(
            model_name='judgementcode',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='judgementcodes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usercode',
            name='user_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usercodes', to=settings.AUTH_USER_MODEL),
        ),
    ]
