# Generated by Django 3.1.3 on 2020-11-20 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gameroom',
            name='finished_at',
        ),
        migrations.AddField(
            model_name='gameroom',
            name='setting',
            field=models.JSONField(blank=True, default=dict, verbose_name='Additional setting for GameRoom'),
        ),
        migrations.AddField(
            model_name='gameroom',
            name='type',
            field=models.CharField(choices=[(None, '(Unknown)'), ('GE', 'General'), ('PR', 'Practice'), ('RA', 'Ranking')], default='GE', max_length=2, verbose_name='Game Type'),
        ),
        migrations.AddField(
            model_name='gameroom',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='gameinfo',
            name='extra_info',
            field=models.JSONField(verbose_name='Additional information of Game'),
        ),
        migrations.AlterField(
            model_name='gameroom',
            name='status',
            field=models.CharField(choices=[(None, '(Unknown)'), ('NS', 'Not started'), ('FN', 'Finished'), ('EO', 'Error occured')], default='NS', max_length=2, verbose_name='Game status'),
        ),
    ]
