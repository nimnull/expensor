from __future__ import absolute_import

from django.conf.urls import patterns, url
from .views import PeopleView, DashboardView

urlpatterns = patterns('core.views',
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^people/$', PeopleView.as_view(), name='people'),
)
