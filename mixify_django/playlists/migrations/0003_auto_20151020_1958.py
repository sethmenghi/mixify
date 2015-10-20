# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0002_auto_20151020_0432'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaylistSong',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField()),
                ('playlist', models.ForeignKey(to='playlists.Playlist')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.RemoveField(
            model_name='song',
            name='playlists',
        ),
        migrations.RemoveField(
            model_name='song',
            name='position',
        ),
        migrations.AddField(
            model_name='playlistsong',
            name='song',
            field=models.ForeignKey(to='playlists.Song'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='songs',
            field=models.ManyToManyField(to='playlists.Song', through='playlists.PlaylistSong'),
        ),
    ]
