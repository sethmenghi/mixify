# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from braces.views import LoginRequiredMixin

from .models import Playlist
from ..users.models import User


class PlaylistUpdateView(LoginRequiredMixin, UpdateView):
    model = Playlist
    # These next two lines tell the view to index lookups by username

    def get_success_url(self):
        return reverse("playlist:detail",
                       kwargs={"playlistname": self.request.playlist.name})

    def get_owner(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)

    def get_object(self):
        return Playlist.objects.get(playlistname=self.request.playlist.name)


class PlaylistListView(LoginRequiredMixin, ListView):
    model = Playlist
    # These next two lines tell the view to index lookups by username
    slug_field = "playlistname"
    slug_url_kwarg = "playlistname"
