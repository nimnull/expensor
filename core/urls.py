from __future__ import absolute_import

from django.conf.urls import patterns, url
from .views import (PeopleView, DashboardView, PersonEdit, PersonDetailView,
                    SettingsView, AccountCreateView, SalaryAddView,
                    ExpenseCategoryAddView)


urlpatterns = patterns('core.views',
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^settings/$', SettingsView.as_view(), name='settings'),

    url(r'^people/$', PeopleView.as_view(), name='people'),
    url(r'^people/(?P<pk>\d+)$', PersonDetailView.as_view(), name='person'),
    url(r'^people/add/$', PersonEdit.as_view(), name='add_person'),
    url(r'^people/edit/(?P<pk>\d+)$', PersonEdit.as_view(), name='edit_person'),

    url(r'^salaries/add/$', SalaryAddView.as_view(), name='add_salary'),

    url(r'^accounts/add/$', AccountCreateView.as_view(), name='add_account'),

    url(r'^expense_categories/add/$', ExpenseCategoryAddView.as_view(),
        name='add_expense_category'),
)
