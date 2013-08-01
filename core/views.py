# -*- encoding: utf-8 -*-
from __future__ import absolute_import

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, edit, DetailView

from .forms import (AccountForm, PersonForm, SalaryForm, ExpenseCategoryForm,
                    CurrencyForm, TransferForm, IncomeTransactionForm,
                    ExpenseTransactionForm)
from .models import (Person, Account, Salary, ExpenseCategory, Currency,
                     Transaction)


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

        context.update({
            'accounts': Account.objects.all(),
            'account_form': AccountForm(),
            'expense_categories': ExpenseCategory.objects.all(),
            'expense_category_form': ExpenseCategoryForm(),
            'currencies': Currency.objects.all(),
            'currency_form': CurrencyForm()
        })

        return context


class DashboardView(AuthRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'


class AccountCreateView(edit.CreateView):
    model = Account
    form_class = AccountForm
    success_url = reverse_lazy('core:settings')


class ExpenseCategoryAddView(AuthRequiredMixin, edit.CreateView):
    model = ExpenseCategory
    success_url = reverse_lazy('core:settings')


class CurrencyAddView(AuthRequiredMixin, edit.CreateView):
    model = Currency
    form_class = CurrencyForm
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


class TransactionListView(AuthRequiredMixin, ListView):
    model = Transaction

    def get_context_data(self, **kwargs):
        context = super(TransactionListView, self).get_context_data(**kwargs)

        initial = {'direction': Transaction.DIRECTION_OUT}
        context['expense_form'] = ExpenseTransactionForm(initial=initial)
        context['transfer_form'] = TransferForm(initial=initial)

        initial = {'direction': Transaction.DIRECTION_IN}
        context['income_form'] = IncomeTransactionForm(initial=initial)

        return context


class TransactionAddView(AuthRequiredMixin, edit.CreateView):
    model = Transaction
    success_url = reverse_lazy('core:transactions')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(TransactionAddView, self).form_valid(form)


class IncomeAddView(TransactionAddView):
    form_class = IncomeTransactionForm


class ExpenseAddView(TransactionAddView):
    form_class = ExpenseTransactionForm


class TransferAddView(TransactionAddView):
    form_class = TransferForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.category = ExpenseCategory.objects.get(
            direct_expense=False, is_transfer=True)
        form.instance.direction = Transaction.DIRECTION_OUT

        Transaction.create_acceptor(form.instance,
                                    form.cleaned_data['account_dst'])
        return super(TransferAddView, self).form_valid(form)
