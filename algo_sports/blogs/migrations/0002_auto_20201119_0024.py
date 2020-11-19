# Generated by Django 3.1.3 on 2020-11-19 00:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='category',
            field=models.SlugField(max_length=2, unique=True, verbose_name='Blog cateogry'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='permission',
            field=models.PositiveSmallIntegerField(choices=[(3, 'Admin only'), (2, 'Staff only'), (1, 'Allow any')], default=1, verbose_name='Blog permission'),
        ),
        migrations.AlterField(
            model_name='post',
            name='blog_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='blogs.blog', verbose_name='Blog of post'),
        ),
    ]