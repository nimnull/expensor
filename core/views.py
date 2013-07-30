# -*- encoding: utf-8 -*-
from __future__ import absolute_import

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, edit, DetailView

from .forms import PersonForm
from .models import Person


class AuthRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AuthRequiredMixin, self).dispatch(request, *args, **kwargs)


class ActionView(AuthRequiredMixin, TemplateView):
    template_name = 'core/actions.html'


class DashboardView(AuthRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'


class PeopleView(AuthRequiredMixin, ListView):
    model = Person

    def get_context_data(self, **kwargs):
        context = super(PeopleView, self).get_context_data(**kwargs)
        return context


class PersonDetail(DetailView):
    model = Person


class PersonEdit(AuthRequiredMixin, edit.CreateView):
    # template_name = 'core/person_form.html'
    model = Person
    success_url = reverse_lazy('core:people')


