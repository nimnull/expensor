from __future__ import absolute_import

from django.conf.urls import patterns, url
from .views import PeopleView, DashboardView, PersonEdit, PersonDetail

urlpatterns = patterns('core.views',
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^people/$', PeopleView.as_view(), name='people'),
    url(r'^person/(?P<pk>\d+)$', PersonDetail.as_view(), name='person'),
    url(r'^person/add/$', PersonEdit.as_view(), name='add_person'),
    url(r'^person/edit/(?P<pk>\d+)$', PersonEdit.as_view(), name='edit_person'),
)
