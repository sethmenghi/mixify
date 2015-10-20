# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from mixify_django import users


@python_2_unicode_compatible
class Playlist(models.Model):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    playlist_id = models.CharField(_("PlaylistID"), blank=False, max_length=255)
    name = models.CharField(_("Name of Playlist"), blank=True, max_length=255)
    owner = models.ForeignKey('users.User')

    def __str__(self):
        return self.name

    @property
    def spotify_object(self):
        return self.owner.spotify_token

    def get_absolute_url(self):
        return reverse('playlist:detail', kwargs={'playlistname': self.name})

    def get_playlists(self, request, token=None, spotify=None):
        if not spotify:
            spotify = self.spotify_object
        playlists = spotify.user_playlists(self.owner.spotify_uid)
        return playlists

    def get_songs(self, spotify=None):
        """Yield all tracks in playlist."""
        if not spotify:
            spotify = self.spotify_object
        results = spotify.user_playlist(self.owner.spotify_uid,
                                        self.playlist_id,
                                        fields='tracks,next')
        tracks = results['tracks']
        for i, item in enumerate(tracks['items']):
            track = item['track']
            yield i, track

    def load_songs(self, spotify=None):
        if not spotify:
            spotify = self.spotify_object
        for i, song in self.get_songs(spotify=spotify):
            artist = song['artists'][0]['name']
            song = Song(song_id=song['id'], name=song['name'], artist=artist,
                        album=song['album'], position=i)
            song.save()
            song.playlists.add(self)
            song.save()

    def add_song(self, song, spotify=None, position=None):
        """Add a song to the playlist."""
        if not spotify:
            spotify = self.spotify_object
        user = self.owner.spotify_username
        spotify.user_playlist_add_tracks(user, self.playlist_id, song, position)


class Song(models.Model):

    song_id = models.CharField(_("SongID"), blank=False, max_length=255)
    name = models.CharField(_("Name of Song"), blank=True, max_length=255)
    artist = models.CharField(_("Name of Artist"), blank=True, max_length=255)
    album = models.CharField(_("Name of Album"), blank=True, max_length=255)
    position = models.IntegerField(_("Track Position"), blank=True)
    playlists = models.ManyToManyField(Playlist)

    def __str__(self):
        return self.name
