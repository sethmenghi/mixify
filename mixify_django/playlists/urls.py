# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the UserListView
    url(
        regex=r'^$',
        view=views.PlaylistListView.as_view(),
        name='list'
    ),

    # URL pattern for the UserRedirectView
    url(
        regex=r'^~redirect/$',
        view=views.PlaylistRedirectView.as_view(),
        name='redirect'
    ),

    # URL pattern for the UserDetailView
    url(
        regex=r'^(?P<playlistname>[\w.@+-]+)/$',
        view=views.PlaylistDetailView.as_view(),
        name='detail'
    ),

    # URL pattern for the UserUpdateView
    url(
        regex=r'^~update/$',
        view=views.PlaylistUpdateView.as_view(),
        name='update'
    ),

    url(
        regex=r'^~load/$',
        view=views.PlaylistLoadView.as_view(),
        name='load'
    ),
]
