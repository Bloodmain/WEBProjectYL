# Generated by Django 3.1.7 on 2021-04-11 14:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0020_auto_20210411_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentary',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 11, 19, 2, 15, 993084), verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='commentary',
            name='unique_parameter',
            field=models.CharField(max_length=100, unique=True, verbose_name='Уникальный параметр'),
        ),
        migrations.AlterField(
            model_name='news',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 11, 19, 2, 15, 990087), verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='repost',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 11, 19, 2, 15, 991086), verbose_name='дата создания'),
        ),
    ]
