# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import logging

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from mixify_django import users


logger = logging.getLogger(__name__)


class Song(models.Model):

    song_id = models.CharField(_("SongID"), unique=True, blank=False, max_length=255)
    name = models.CharField(_("Name of Song"), blank=True, max_length=255)
    artist = models.CharField(_("Name of Artist"), blank=True, max_length=255)
    album = models.CharField(_("Name of Album"), blank=True, max_length=255)
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """To make sure slug gets saved correctly."""
        if not self.id and not self.slug:
            slug = slugify(self.name)
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exists = Song.objects.get(slug=slug)
                    if slug_exists:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except Song.DoesNotExist:
                    self.slug = slug
                    break
        super(Song, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Playlist(models.Model):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    playlist_id = models.CharField(_("PlaylistID"), blank=False, max_length=255)
    name = models.CharField(_("Name of Playlist"), blank=True, max_length=255)
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    owner = models.ForeignKey('users.User')
    songs = models.ManyToManyField(Song, through='PlaylistSong')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """To make sure slug gets saved correctly."""
        if not self.id and not self.slug:
            slug = slugify(self.name)
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exists = Playlist.objects.get(slug=slug)
                    if slug_exists:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except Playlist.DoesNotExist:
                    self.slug = slug
                    break
        super(Playlist, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('playlist:detail', kwargs={'slug': self.slug})

    @property
    def spotify_object(self):
        return self.owner.spotify_token

    @property
    def songs_by_position(self):
        return self.song_set.order_by('position')

    @property
    def local_songs(self):
        playlistsongs = Song.objects.filter(playlist__playlist_id=self.playlist_id)
        return playlistsongs

    def save_to_playlist(self, song, position):
        playlistsong = PlaylistSong(playlist=self, song=song, position=position)
        playlistsong.save()

    def is_song_inside(self, song):
        """Check if a spotify song object is in this playlist."""
        song = self.song_set.filter(song_id=song['id']).first()
        if song:
            return True
        else:
            return False

    def get_songs_from_spotify(self, username=None, spotify=None):
        """Yield all tracks in the playlists id."""
        if not spotify:
            spotify = self.spotify_object
        if not username:
            username = self.owner.spotify_uid
        results = spotify.user_playlist(username, self.playlist_id,
                                        fields='tracks,next')
        tracks = results['tracks']
        for item in tracks['items']:
            track = item['track']
            if track['id']:  # Song is a localfile, can't add
                yield track

    def load_songs(self, username=None, spotify=None):
        """Load songs into a new playlist."""
        if not spotify:
            spotify = self.spotify_object
        songs_positioned = enumerate(self.get_songs_from_spotify(spotify=spotify))
        for i, song in songs_positioned:
            logger.debug(i, song['id'], song['name'], song['album'])
            if song['id']:
                artist = song['artists'][0]['name']
                song_obj = Song.objects.filter(song_id=song['id']).first()
                if not song_obj:  # Song is new to the database
                    song_obj = Song(song_id=song['id'], name=song['name'], artist=artist,
                                    album=song['album']['name'])
                    song_obj.save()
                self.save_to_playlist(song_obj, i)

    def reload_songs(self, username=None, spotify=None):
        """Completely reload playlist from spotify."""
        if not spotify:
            spotify = self.spotify_object
        songs_positioned = enumerate(self.get_songs_from_spotify(spotify=spotify))
        for i, song in songs_positioned:
            if song['id']:  # make sure song isn't a local file
                song_obj = Song.objects.filter(song_id=song['id']).first()
                playlist_song = PlaylistSong.objects.filter(playlist=self, song=song).first()
                if song_obj and playlist_song:  # song exists in db  and song already in playlist
                    playlist_song.position = i
                elif song_obj:
                    self.save_to_playlist(song_obj, i)
                else:
                    song_obj = Song(song_id=song['id'], name=song['name'],
                                    artist=song['artists'][0]['name'],
                                    album=song['album']['name'])
                    song_obj.save()
                    self.save_to_playlist(song_obj, i)

    def add_song(self, song, spotify=None, position=None):
        """Add a song to the playlist."""
        if not spotify:
            spotify = self.spotify_object
        user = self.owner.spotify_username
        spotify.user_playlist_add_tracks(user, self.playlist_id, song, position)


class PlaylistSong(models.Model):
    """Need an intermediate table to support position in the playlist."""
    playlist = models.ForeignKey('playlists.Playlist')
    song = models.ForeignKey('playlists.Song')
    position = models.IntegerField()

    class Meta:
        ordering = ['position']
