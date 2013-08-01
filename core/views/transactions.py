from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, edit
from core.forms import (ExpenseTransactionForm, TransferForm,
                        IncomeTransactionForm)

from core.models import Transaction, ExpenseCategory
from core.views.base import AuthRequiredMixin

__author__ = 'nimnull'


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
