# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0004_playlist_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='owner',
        ),
    ]
