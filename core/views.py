# -*- encoding: utf-8 -*-
from __future__ import absolute_import

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView

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
        context['person_form'] = PersonForm()
        return context


class PeopleEdit(AuthRequiredMixin, TemplateView):
    template_name = 'core/person_form.html'


    def get(self, request, *args, **kwargs):
        person_id = kwargs.get('id')
        if person_id is None:
            return self.render_to_response({})
        else:
            return self.render_to_response({})

