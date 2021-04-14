# Generated by Django 3.1.7 on 2021-04-11 18:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0022_auto_20210411_2226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentary',
            name='unique_parameter',
        ),
        migrations.AlterField(
            model_name='commentary',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 11, 23, 6, 49, 98416), verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='news',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 11, 23, 6, 49, 97416), verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='repost',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 11, 23, 6, 49, 97416), verbose_name='дата создания'),
        ),
    ]