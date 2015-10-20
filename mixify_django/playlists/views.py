# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from braces.views import LoginRequiredMixin

# from .models import Playlist
from ..users.models import User
from .models import Playlist


class PlaylistListView(LoginRequiredMixin, ListView):
    model = Playlist

    # These next two lines tell the view to index lookups by username
    slug_field = "slug"
    slug_url_kwarg = "slug"


class PlaylistDetailView(LoginRequiredMixin, DetailView):
    model = Playlist
    # These next two lines tell the view to index lookups by username
    slug_field = "slug"
    slug_url_kwarg = "slug"


class PlaylistRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("playlists:list")


class PlaylistUpdateView(LoginRequiredMixin, UpdateView):
    model = Playlist
    # These next two lines tell the view to index lookups by username

    def get_success_url(self):
        playlist = Playlist.objects.get(id=self.kwargs['id']).first()
        return reverse("playlists:detail",
                       kwargs={"slug": playlist.slug})

    def get_owner(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)

    def get_object(self):
        return Playlist.objects.get(id=self.kwargs['id'],
                                    owner=self.get_owner())


def load_playlists(request):
    request.user.load_playlists()
    return reverse("users:list")
