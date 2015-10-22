# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    # URL pattern for the MixtapeListView
    url(
        regex=r'^$',
        view=views.MixtapeListView.as_view(),
        name='list'
    ),

    # URL pattern for the MixtapeRedirectView
    url(
        regex=r'^~redirect/$',
        view=views.MixtapeRedirectView.as_view(),
        name='redirect'
    ),

    # URL pattern for the MixtapeDetailView
    url(
        regex=r'^(?P<slug>[-\w\d]+)/$',
        view=views.MixtapeDetailView.as_view(),
        name='detail'
    ),

    # URL pattern for the MixtapeUpdateView
    url(
        regex=r'^~update/$',
        view=views.MixtapeUpdateView.as_view(),
        name='update'
    ),

    # URL pattern to view all Mixtapes MixtapeListAllView
    url(
        regex=r'^~all/$',
        view=views.MixtapeListAllView.as_view(),
        name='all'
    ),

    url(
        regex=r'^~new/$',
        view=views.MixtapeCreate.as_view(),
        name='new'
    ),
]
