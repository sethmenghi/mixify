# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, CreateView
from django.shortcuts import redirect

from braces.views import LoginRequiredMixin

# from .models import Mixtape
from ..users.models import User
from .models import Mixtape


class MixtapeListAllView(LoginRequiredMixin, ListView):
    model = Mixtape
    template_name = 'mixtapes/mixtape_all.html'
    slug_field = "slug"
    slug_url_kwarg = "slug"


class MixtapeListView(LoginRequiredMixin, ListView):
    model = Mixtape

    # These next two lines tell the view to index lookups by username
    slug_field = "slug"
    slug_url_kwarg = "slug"


class MixtapeDetailView(LoginRequiredMixin, DetailView):
    model = Mixtape
    # These next two lines tell the view to index lookups by username
    slug_field = "slug"
    slug_url_kwarg = "slug"


class MixtapeRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("mixtapes:list")


class MixtapeCreate(CreateView):
    model = Mixtape
    fields = ['name', 'owner']

    def get_initial(self):
        return {'owner': self.request.user}

    def get_success_url(self):
        mixtape = Mixtape.objects.get(id=self.kwargs['id']).first()
        return reverse("mixtapes:list")
                      #  kwargs={"slug": mixtape.slug})


# Will be where to add songs or create a new view add button to list view?
class MixtapeUpdateView(LoginRequiredMixin, UpdateView):
    model = Mixtape
    # These next two lines tell the view to index lookups by username

    def get_success_url(self):
        mixtape = Mixtape.objects.get(id=self.kwargs['id']).first()
        return reverse("mixtapes:detail",
                       kwargs={"slug": mixtape.slug})

    def get_owner(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)

    def get_object(self):
        return Mixtape.objects.get(id=self.kwargs['id'],
                                   owner=self.get_owner())
