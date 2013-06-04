from __future__ import absolute_import

from django.conf.urls import patterns, url
from .views import PeopleView, DashboardView, PeopleEdit

urlpatterns = patterns('core.views',
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^people/$', PeopleView.as_view(), name='people'),
    url(r'^people/add/$', PeopleEdit.as_view(), name='people_add'),
    url(r'^people/edit/(?P<id>\d+)$', PeopleEdit.as_view(), name='people_edit'),
)
