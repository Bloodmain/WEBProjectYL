# Generated by Django 3.1.7 on 2021-04-11 17:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0021_merge_20210411_0107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentary',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 11, 22, 26, 54, 822790), verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='commentary',
            name='text',
            field=models.TextField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='commentary',
            name='unique_parameter',
            field=models.CharField(max_length=100, unique=True, verbose_name='Уникальный параметр'),
        ),
        migrations.AlterField(
            model_name='news',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 11, 22, 26, 54, 820791), verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='repost',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 11, 22, 26, 54, 821791), verbose_name='дата создания'),
        ),
    ]
