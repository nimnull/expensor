from django.core.urlresolvers import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, edit
from core.forms import (ExpenseTransactionForm, TransferForm,
                        IncomeTransactionForm, CommissionForm, PaymentForm)

from core.models import Transaction, ExpenseCategory, Person
from core.views.base import AuthRequiredMixin

__author__ = 'nimnull'


class TransactionListView(AuthRequiredMixin, ListView):
    """ Full list of transactions
    """
    model = Transaction
    # queryset = Transaction.objects.filter(parent__isnull=True).order_by('-bill_date')

    def get_context_data(self, **kwargs):
        context = super(TransactionListView, self).get_context_data(**kwargs)

        initial = {'direction': Transaction.DIRECTION_OUT}
        context['expense_form'] = ExpenseTransactionForm(initial=initial)
        context['transfer_form'] = TransferForm(initial=initial)

        initial = {'direction': Transaction.DIRECTION_IN}
        context['income_form'] = IncomeTransactionForm(initial=initial)

        context['commission_form'] = CommissionForm()
        

        transactions = []
        monthes = Transaction.objects.dates("bill_date", "month")
        for month in monthes:
            month_payments = Transaction.objects.filter(bill_date__month=month.month).order_by('-bill_date')
            transactions.append({'month': month.strftime("%Y %m"), 'transactions': month_payments })
        transactions = sorted(transactions, key=lambda k: k['month'], reverse=True)


        paginator = Paginator(transactions, 2)
        page = self.request.GET.get('page')
        try:
            paged_trans = paginator.page(page)
        except PageNotAnInteger:            
            paged_trans = paginator.page(1)
        except EmptyPage:            
            paged_trans = paginator.page(paginator.num_pages)

        context['transactions'] = paged_trans

        return context


class TransactionAddView(AuthRequiredMixin, edit.CreateView):
    """ Base class for adding varous transaction types
    """
    model = Transaction
    success_url = reverse_lazy('core:transactions')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(TransactionAddView, self).form_valid(form)


class IncomeAddView(TransactionAddView):
    """ View for creating income
    """
    form_class = IncomeTransactionForm


class ExpenseAddView(TransactionAddView):
    """ View class for creating expense
    """
    form_class = ExpenseTransactionForm


class TransferAddView(TransactionAddView):
    """ View for creating transfer between accounts
    """
    form_class = TransferForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.category = ExpenseCategory.get_transfer()
        form.instance.direction = Transaction.DIRECTION_OUT
        response = super(TransferAddView, self).form_valid(form)
        Transaction.create_acceptor(self.object,
                                    form.cleaned_data['account_dst'])
        return response


class CommissionAddView(TransactionAddView):
    """ View for creating commissions
    """
    form_class = CommissionForm


    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        self.parent_transaction = Transaction.objects.get(pk=kwargs['pk'])
        return super(CommissionAddView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.parent = self.parent_transaction
        form.instance.category = ExpenseCategory.get_commission()
        form.instance.account = self.parent_transaction.account
        form.instance.direction = Transaction.DIRECTION_OUT
        form.instance.bill_date = self.parent_transaction.bill_date
        return super(CommissionAddView, self).form_valid(form)


class PaymentAddView(TransactionAddView):
    form_class = PaymentForm
    success_url = reverse_lazy('core:people')

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        self.person = Person.objects.get(pk=kwargs['pk'])
        return super(PaymentAddView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.category = ExpenseCategory.get_payment()
        form.instance.direction = Transaction.DIRECTION_OUT
        form.instance.person = self.person
        return super(PaymentAddView, self).form_valid(form)
