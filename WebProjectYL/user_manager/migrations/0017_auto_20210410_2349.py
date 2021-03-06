# Generated by Django 3.1.7 on 2021-04-10 18:49

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0016_auto_20210407_2144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posts',
            old_name='repost',
            new_name='reposts',
        ),
        migrations.RemoveField(
            model_name='commentary',
            name='news',
        ),
        migrations.RemoveField(
            model_name='repost',
            name='news',
        ),
        migrations.AddField(
            model_name='commentary',
            name='post',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='user_manager.posts'),
        ),
        migrations.AddField(
            model_name='commentary',
            name='unique_parameter',
            field=models.IntegerField(default=0, unique=True, verbose_name='Уникальный параметр'),
        ),
        migrations.AddField(
            model_name='repost',
            name='posts',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, related_name='repost', to='user_manager.posts'),
        ),
        migrations.AlterField(
            model_name='likes',
            name='unique_parameter',
            field=models.CharField(blank=True, max_length=50, unique=True, verbose_name='Уникальный параметр'),
        ),
        migrations.AlterField(
            model_name='news',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 10, 23, 49, 23, 643440), verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='repost',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 10, 23, 49, 23, 644439), verbose_name='дата создания'),
        ),
    ]
