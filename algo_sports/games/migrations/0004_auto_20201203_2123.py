# Generated by Django 3.1.3 on 2020-12-03 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_auto_20201130_0130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gameroom',
            name='gameinfo_id',
        ),
        migrations.AddField(
            model_name='gameroom',
            name='gameversion_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='game_rooms', to='games.gameversion', verbose_name='Game Version'),
            preserve_default=False,
        ),
    ]
