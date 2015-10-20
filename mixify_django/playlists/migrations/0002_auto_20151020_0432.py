# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='song_id',
            field=models.CharField(unique=True, max_length=255, verbose_name='SongID'),
        ),
    ]
