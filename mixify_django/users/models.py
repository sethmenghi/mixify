# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from spotipy import util
import spotipy


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    spotify_username = models.CharField(_("Spotify Username"), blank=True, max_length=255)
    client_id = models.CharField(_("ClientID"), blank=True, max_length=255)
    client_secret = models.CharField(_("ClientSecret"), blank=True, max_length=255)
    token = None

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def get_spotipy_token(self):
        scope = 'playlist-modify-public'
        if self.token is None:
            self.token = util.prompt_for_user_token(username=self.spotify_username,
                                                    scope=scope)
        return self.token

    def load_playlists(self):
        token = self.get_spotipy_token()
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(self.owner.spotify_username)
        for playlist in playlists['items']:
            print
            print playlist['name']
            self.load_playlist(playlist)

    def load_playlist(self, playlist):
        playlist_id = playlist['id']
        name = playlist['name']
        playlist = Playlist(playlist_id=playlist_id, name=name, owner=self)
        playlist.save()
        playlist.load_songs()


@python_2_unicode_compatible
class Playlist(models.Model):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    playlist_id = models.CharField(_("PlaylistID"), blank=False, max_length=255)
    name = models.CharField(_("Name of Playlist"), blank=True, max_length=255)
    owner = models.ForeignKey(User, related_name='owner')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('playlist:detail', kwargs={'playlistname': self.name})

    def get_playlists(self):
        token = self.owner.get_spotipy_token()
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(self.owner.spotify_username)
        return playlists

    def get_songs(self):
        """Yield all tracks in playlist."""
        token = self.owner.get_spotipy_token()
        sp = spotipy.Spotify(auth=token)
        results = sp.user_playlist(self.owner.spotify_username, self.playlist_id,
                                   fields='tracks.next')
        tracks = results['tracks']
        for i, item in enumerate(tracks['items']):
            track = item['track']
            yield i, track

    def load_songs(self):
        for i, song in self.get_songs():
            artist = song['artists'][0]['name']
            song = Song(song_id=song['id'], name=song['name'], artist=artist,
                        album=song['album'], position=i)
            song.save()
            song.playlists.add(self)
            song.save()

    def add_song(self, song, position=None):
        """Add a song to the playlist."""
        token = self.owner.get_spotipy_token()
        sp = spotipy.Spotify(auth=token)
        user = self.owner.spotify_username
        sp.user_playlist_add_tracks(user, self.playlist_id, song, position)


class Song(models.Model):

    song_id = models.CharField(_("SongID"), blank=False, max_length=255)
    name = models.CharField(_("Name of Song"), blank=True, max_length=255)
    artist = models.CharField(_("Name of Artist"), blank=True, max_length=255)
    album = models.CharField(_("Name of Album"), blank=True, max_length=255)
    position = models.IntegerField(_("Track Position"), blank=True, max_length=255)
    playlists = models.ManyToManyField(Playlist)

    def __str__(self):
        return self.name
