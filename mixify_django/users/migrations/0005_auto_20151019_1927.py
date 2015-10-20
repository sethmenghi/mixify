# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '__first__'),
        ('users', '0004_playlist_song'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='song',
            name='playlists',
        ),
        migrations.AddField(
            model_name='user',
            name='playlists',
            field=models.ManyToManyField(to='playlists.Playlist'),
        ),
        migrations.DeleteModel(
            name='Playlist',
        ),
        migrations.DeleteModel(
            name='Song',
        ),
    ]
