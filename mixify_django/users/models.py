# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import logging

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from allauth.socialaccount.models import SocialToken, SocialAccount

from spotipy import util
import spotipy

from ..playlists.models import Playlist


logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

    def _get_spotify_token(self):
        access_token = SocialToken.objects.filter(account__provider='spotify',
                                                  account__user=self).first()
        token = str(access_token.token)
        return token

    def _get_spotify_object(self):
        return spotipy.Spotify(auth=self.access_token)

    @property
    def access_token(self):
        return self._get_spotify_token()

    @property
    def spotify_object(self):
        return self._get_spotify_object()

    @property
    def spotify_account(self):
        social_account = SocialAccount.objects.filter(provider='spotify',
                                                      user=self).first()
        return social_account

    @property
    def spotify_uid(self):
        social_account = self.spotify_account
        return str(social_account.uid)

    def load_playlists(self):
        # spotify = self.spotify_object
        spotify = self.spotify_object
        playlists = spotify.user_playlists(self.spotify_uid)
        for playlist in playlists['items']:
            print(playlist['id'], playlist['name'])
            if 'Radio' not in playlist['name']:
                self.load_playlist(playlist, spotify=spotify)

    def load_playlist(self, playlist, spotify=None):
        print(playlist['owner'])
        owner_id = playlist['owner']['id']
        if owner_id == self.spotify_uid:
            if not spotify:
                spotify = self.spotify_object
            playlist_id = playlist['id']
            name = playlist['name']
            playlist = Playlist(playlist_id=playlist_id, name=name, owner=self)
            playlist.save()
            playlist.load_songs(spotify=spotify)
