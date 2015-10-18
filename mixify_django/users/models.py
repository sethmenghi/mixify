# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from spotipy import util
import spotipy

from ..playlist.models import Playlist


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    spotify_username = models.CharField(_("Spotify Username"), blank=True, max_length=255)
    client_id = models.CharField(_("ClientID"), blank=True, max_length=255)
    client_secret = models.CharField(_("ClientSecret"), blank=True, max_length=255)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def get_spotipy_token(self):
        scope = 'playlist-modify-public'
        token = util.prompt_for_user_token(self.spotify_username, scope)
        return token

    def load_playlists(self):
        token = self.user.get_spotipy_token()
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
