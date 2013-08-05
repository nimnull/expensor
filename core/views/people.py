from django.views.generic import ListView, DetailView, edit
from core.forms import PersonForm, SalaryForm, PaymentForm
from core.models import Person, Salary
from core.views.base import AuthRequiredMixin

__author__ = 'nimnull'


class PeopleView(AuthRequiredMixin, ListView):
    model = Person

    def get_context_data(self, **kwargs):
        context = super(PeopleView, self).get_context_data(**kwargs)
        context['person_form'] = PersonForm()
        context['payment_form'] = PaymentForm()
        return context


class PersonDetailView(DetailView):
    model = Person

    def get_context_data(self, **kwargs):
        person = kwargs['object']
        context = super(PersonDetailView, self).get_context_data(**kwargs)
        context['salary_form'] = SalaryForm(initial={'person': person})

        return context


class PersonEdit(AuthRequiredMixin, edit.CreateView):
    model = Person
    form_class = PersonForm


class SalaryAddView(AuthRequiredMixin, edit.CreateView):
    model = Salary
    form_class = SalaryForm
