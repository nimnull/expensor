# encoding: utf-8
from __future__ import absolute_import
from django import forms
from .models import Person, Account, Salary


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
