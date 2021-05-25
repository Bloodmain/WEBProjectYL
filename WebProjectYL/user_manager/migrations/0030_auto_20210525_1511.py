# Generated by Django 3.1.7 on 2021-05-25 10:11

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_manager', '0029_auto_20210525_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='communities_creator', to=settings.AUTH_USER_MODEL),
        )
    ]
