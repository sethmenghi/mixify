# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_spotify_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('playlist_id', models.CharField(max_length=255, verbose_name='PlaylistID')),
                ('name', models.CharField(max_length=255, verbose_name='Name of Playlist', blank=True)),
                ('owner', models.ForeignKey(related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('song_id', models.CharField(max_length=255, verbose_name='SongID')),
                ('name', models.CharField(max_length=255, verbose_name='Name of Song', blank=True)),
                ('artist', models.CharField(max_length=255, verbose_name='Name of Artist', blank=True)),
                ('album', models.CharField(max_length=255, verbose_name='Name of Album', blank=True)),
                ('position', models.IntegerField(max_length=255, verbose_name='Track Position', blank=True)),
                ('playlists', models.ManyToManyField(to='users.Playlist')),
            ],
        ),
    ]
