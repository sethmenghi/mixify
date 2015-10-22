# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin

from .models import Song, Mixtape, MixtapeSong

admin.site.register(Mixtape)
admin.site.register(MixtapeSong)
