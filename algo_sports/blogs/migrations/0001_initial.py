# Generated by Django 3.1.3 on 2020-11-17 21:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=2, verbose_name='Blog cateogry')),
                ('permission', models.CharField(choices=[('AD', 'Admin only'), ('ST', 'Staff only'), ('AL', 'Allow any')], default='AL', max_length=2, verbose_name='Blog permission')),
                ('description', models.TextField(max_length=2, verbose_name='Blog description')),
            ],
            options={
                'ordering': ['category'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='Post title')),
                ('content', models.TextField(verbose_name='Post content')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('blog_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='blogs.blog', verbose_name='Post of comment')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Post author')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False, verbose_name='Is Comment deleted?')),
                ('content', models.CharField(max_length=300, verbose_name='Comment content')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='childs', to='blogs.comment', verbose_name='Parent Comment')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comments', to='blogs.post', verbose_name='Comment of post')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Comment author')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]