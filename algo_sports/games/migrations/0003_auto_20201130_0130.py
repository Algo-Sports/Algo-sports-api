# Generated by Django 3.1.3 on 2020-11-30 01:30

import algo_sports.games.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20201120_1723'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gameinfo',
            options={'ordering': ['title']},
        ),
        migrations.RemoveField(
            model_name='gameinfo',
            name='version',
        ),
        migrations.AlterField(
            model_name='gameinfo',
            name='title',
            field=models.CharField(max_length=50, unique=True, verbose_name='Game title'),
        ),
        migrations.CreateModel(
            name='GameVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.JSONField(default=algo_sports.games.models.get_default_version, verbose_name='Game Version')),
                ('change_log', models.JSONField(default=dict, verbose_name='Version change log')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is this version active?')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('gameinfo_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='versions', to='games.gameinfo', verbose_name='Game information')),
            ],
            options={
                'ordering': ['version__micro', 'version__minor', 'version__major'],
                'unique_together': {('gameinfo_id', 'version')},
            },
        ),
    ]
