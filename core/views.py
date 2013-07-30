# -*- encoding: utf-8 -*-
from __future__ import absolute_import

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, edit, DetailView

from .forms import AccountForm, PersonForm
from .models import Person, Account


class AuthRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AuthRequiredMixin, self).dispatch(request, *args, **kwargs)


class ActionView(AuthRequiredMixin, TemplateView):
    template_name = 'core/actions.html'


class SettingsView(AuthRequiredMixin, TemplateView):
    template_name = 'core/settings.html'

    def get_context_data(self, **kwargs):
        context = super(SettingsView, self).get_context_data(**kwargs)
        context['accounts'] = Account.objects.all()
        context['account_form'] = AccountForm()
        return context


class DashboardView(AuthRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'


class AccountCreateView(edit.CreateView):
    model = Account
    form_class = AccountForm
    success_url = reverse_lazy('core:settings')


class PeopleView(AuthRequiredMixin, ListView):
    model = Person

    def get_context_data(self, **kwargs):
        context = super(PeopleView, self).get_context_data(**kwargs)
        context['person_form'] = PersonForm()
        return context


class PersonDetailView(DetailView):
    model = Person

    def get_context_data(self, **kwargs):
        # person = kwargs['object']
        context = super(PersonDetailView, self).get_context_data(**kwargs)
        return context


class PersonEdit(AuthRequiredMixin, edit.CreateView):
    # template_name = 'core/person_form.html'
    model = Person
    form_class = PersonForm
    success_url = reverse_lazy('core:people')


