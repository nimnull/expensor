# encoding: utf-8
from __future__ import absolute_import
from decimal import Decimal
from django import forms
from django.contrib.contenttypes.models import ContentType
from .models import Person, Account, Salary, ExpenseCategory, Currency, Transaction


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        exclude = ('notes',)


class AccountForm(forms.ModelForm):

    class Meta:
        model = Account
        exclude = ('amount', 'comment')


class SalaryForm(forms.ModelForm):

    class Meta:
        model = Salary
        widgets = {
            'person': forms.HiddenInput
        }


class ExpenseCategoryForm(forms.ModelForm):

    class Meta:
        model = ExpenseCategory


class CurrencyForm(forms.ModelForm):

    class Meta:
        model = Currency


class TransactionForm(forms.ModelForm):

    ratio = forms.ChoiceField(label=u'валюта', choices=Currency.objects.values_list('ratio', 'name'))

    class Meta:
        model = Transaction
        exclude = ('amount', 'created_at', 'created_by',)
        widgets = {
            'direction': forms.HiddenInput
        }
