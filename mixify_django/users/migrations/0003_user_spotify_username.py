# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20151018_2131'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='spotify_username',
            field=models.CharField(max_length=255, verbose_name='Spotify Username', blank=True),
        ),
    ]
