# encoding: utf-8
from __future__ import absolute_import
# from decimal import Decimal
from django import forms
# from django.contrib.contenttypes.models import ContentType
from .models import Person, Account, Salary, ExpenseCategory, Currency, Transaction, Candidate


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        exclude = ('notes', )


class CandidateForm(forms.ModelForm):

    class Meta:
        model = Candidate
        exclude = ('person', )


class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        exclude = ('amount', 'comment')


class SalaryForm(forms.ModelForm):

    class Meta:
        model = Salary
        exclude = ('created_at', )
        widgets = {
            'person': forms.HiddenInput
        }


class ExpenseCategoryForm(forms.ModelForm):

    class Meta:
        model = ExpenseCategory


class CurrencyForm(forms.ModelForm):

    class Meta:
        model = Currency


class IncomeTransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        exclude = ('amount', 'created_at', 'created_by', 'person', 'category',
                   'parent', 'ratio')
        widgets = {
            'direction': forms.HiddenInput
        }


class ExpenseTransactionForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=ExpenseCategory.objects.filter(direct_expense=True,
                                                is_transfer=False))

    class Meta(IncomeTransactionForm.Meta):
        exclude = ('amount', 'created_at', 'created_by', 'person', 'parent',
                   'ratio')


class TransferForm(forms.ModelForm):
    account = forms.ModelChoiceField(
        label=u'источник',
        queryset=Account.objects.all())
    account_dst = forms.ModelChoiceField(
        label=u'назначение',
        queryset=Account.objects.all())

    class Meta(IncomeTransactionForm.Meta):
        widgets = {
            'direction': forms.HiddenInput,
            'category': forms.HiddenInput
        }


class CommissionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ('currency', 'amount_src')


class PaymentForm(forms.ModelForm):
    account = forms.ModelChoiceField(label=u'источник',
                                     queryset=Account.objects.all())

    class Meta:
        model = Transaction
        fields = ('account', 'currency', 'amount_src')
