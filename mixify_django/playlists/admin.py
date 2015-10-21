# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin

from .models import Song, Playlist, PlaylistSong

admin.site.register(Song)
admin.site.register(Playlist)
admin.site.register(PlaylistSong)
