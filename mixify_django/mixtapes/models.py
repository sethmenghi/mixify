# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
import logging

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from ..playlists.models import Song


@python_2_unicode_compatible
class Mixtape(models.Model):

    name = models.CharField(_("Name of Mixtape"), blank=True, max_length=255)
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    owner = models.ForeignKey('users.User')
    songs = models.ManyToManyField(Song, through='MixtapeSong')
    provider_id = models.CharField(_("ID given by provider"), blank=True, max_length=255)

    def __str__(self):
        return self.name

    @property
    def local_songs(self):
        """Return all songs in database."""
        mixtapesongs = Song.objects.filter(mixtape__provider_id=self.provider_id)
        return mixtapesongs

    @property
    def length(self):
        return Song.objects.filter(mixtape__provider_id=self.provider_id).count

    def init_spotify(self):
        """Create playlist on spotify as name."""
        spotify = self.owner.spotify_object()
        if self.provider_id is None:
            playlist = spotify.user_playlist_create(self.owner.spotify_uid, self.name)
            self.provider_id = playlist['id']

    def save_song(self, song, position):
        mixtapesong = MixtapeSong(mixtape=self, song=song, position=position)
        mixtapesong.save()

    def update_spotify_playlist(self):
        spotify = self.owner.spotify_object()
        if self.provider_id is None:
            playlist = spotify.user_playlist_create(self.owner.spotify_uid, self.name)
            self.provider_id = playlist['id']
            for song in self.local_songs:
                spotify.user_playlist_add_track(self.owner.spotify_uid,
                                                self.provider_id, song.song_id)
        else:  # Reorder tracks
            self.reorder_tracks()

    def reorder_tracks(self):
        """NEEDS BETTER ALGORITHM."""
        spotify = self.owner.spotify_object()
        for song in self.local_songs:
            spotify.user_playlist_remove_all_occurrences_of_tracks(self.owner.spotify_uid,
                                                                   self.provider_id, song.song_id)
        for song in self.local_songs:
            spotify.user_playlist_add_track(self.owner.spotify_uid,
                                            self.provider_id, song.song_id)

    def init_slug(self):
        if not self.id and not self.slug:
            slug = slugify(self.name)
            slug_exists = True
            counter = 1
            self.slug = slug
            while slug_exists:
                try:
                    slug_exists = Mixtape.objects.get(slug=slug)
                    if slug_exists:
                        slug = self.slug + '_' + str(counter)
                        counter += 1
                except Mixtape.DoesNotExist:
                    self.slug = slug
                    break

    def save(self, *args, **kwargs):
        """To make sure slug gets saved correctly."""
        self.init_slug()
        self.init_spotify()
        super(Mixtape, self).save(*args, **kwargs)


@python_2_unicode_compatible
class MixtapeSong(models.Model):
    """Need an intermediate table to support position in the mixtape."""
    mixtape = models.ForeignKey('mixtapes.Mixtape')
    song = models.ForeignKey('playlists.Song')
    position = models.IntegerField()
    votes = models.IntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['position']

    def upvote(self):
        self.votes += 1
        if self.position > 0:
            higher_song = MixtapeSong.objects.filter(mixtape=self.mixtape, position=self.position)
            if self.votes > higher_song.votes:
                higher_song.votes.position = self.position
                self.position -= 1
                self.mixtape.reorder_tracks()

    def downvote(self):
        self.votes -= 1
