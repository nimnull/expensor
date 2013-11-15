from django.views.generic import ListView, DetailView, edit
from core.forms import PersonForm, SalaryForm, PaymentForm, CandidateForm
from core.models import Person, Salary, Currency, Candidate
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
        context['payment_form'] = PaymentForm(initial={'currency': Currency.default(),
                                                       'amount_src': person.salary.amount})
        return context


class PersonEdit(AuthRequiredMixin, edit.CreateView):
    model = Person
    form_class = PersonForm


class SalaryAddView(AuthRequiredMixin, edit.CreateView):
    model = Salary
    form_class = SalaryForm



class CandidateView(AuthRequiredMixin, ListView):
    model = Candidate

    def get_context_data(self, **kwargs):
        context = super(CandidateView, self).get_context_data(**kwargs)
        context['person_form'] = CandidateForm()
        return context


class CandidateDetailView(DetailView):
    model = Candidate

    # def get_context_data(self, **kwargs):
    #     person = kwargs['object']
    #     context = super(PersonDetailView, self).get_context_data(**kwargs)
    #     context['salary_form'] = SalaryForm(initial={'person': person})
    #     context['payment_form'] = PaymentForm(initial={'currency': Currency.default(),
    #                                                    'amount_src': person.salary.amount})
    #     return context


class CandidateEdit(AuthRequiredMixin, edit.CreateView):
    model = Candidate
    form_class = CandidateForm