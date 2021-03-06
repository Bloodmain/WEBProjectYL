# Generated by Django 3.1.7 on 2021-05-25 19:19

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_manager', '0031_auto_20210525_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='admins',
            field=models.ManyToManyField(null=True, related_name='communities_admin', to=settings.AUTH_USER_MODEL, verbose_name='Админы'),
        ),
        migrations.AlterField(
            model_name='community',
            name='members',
            field=models.ManyToManyField(null=True, related_name='communities', to=settings.AUTH_USER_MODEL, verbose_name='Подписчики'),
        ),
    ]
