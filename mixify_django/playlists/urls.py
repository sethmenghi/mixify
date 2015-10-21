# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the PlaylistListView
    url(
        regex=r'^$',
        view=views.PlaylistListView.as_view(),
        name='list'
    ),

    # URL pattern for the PlaylistRedirectView
    url(
        regex=r'^~redirect/$',
        view=views.PlaylistRedirectView.as_view(),
        name='redirect'
    ),

    # URL pattern for the PlaylistDetailView
    url(
        regex=r'^(?P<slug>[-\w\d]+)/$',
        view=views.PlaylistDetailView.as_view(),
        name='detail'
    ),

    # URL pattern for the PlaylistUpdateView
    url(
        regex=r'^~update/$',
        view=views.PlaylistUpdateView.as_view(),
        name='update'
    ),

    # URL pattern to view all playlists PlaylistListAllView
    url(
        regex=r'^~all/$',
        view=views.PlaylistListAllView.as_view(),
        name='all'
    ),

    url(
        regex=r'^~load/$',
        view=views.load_playlists,
        name='load'
    ),
]
