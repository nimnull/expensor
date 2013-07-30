from __future__ import absolute_import

from django.conf.urls import patterns, url
from .views import (PeopleView, DashboardView, PersonEdit, PersonDetailView,
                    SettingsView, AccountCreateView)

urlpatterns = patterns('core.views',
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^settings/$', SettingsView.as_view(), name='settings'),

    url(r'^people/$', PeopleView.as_view(), name='people'),
    url(r'^person/(?P<pk>\d+)$', PersonDetailView.as_view(), name='person'),
    url(r'^person/add/$', PersonEdit.as_view(), name='add_person'),
    url(r'^person/edit/(?P<pk>\d+)$', PersonEdit.as_view(), name='edit_person'),

    url(r'^account/add/$', AccountCreateView.as_view(), name='add_account'),

)
