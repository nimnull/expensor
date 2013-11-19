from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, DetailView, edit
from core.forms import AccountForm, ExpenseCategoryForm, CurrencyForm
from core.models import Account, ExpenseCategory, Currency
from core.views.base import AuthRequiredMixin

__author__ = 'nimnull'


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


class ExpenseCategoryView(AuthRequiredMixin, DetailView):
    model = ExpenseCategory

    def get_context_data(self, **kwargs):
        # expence = kwargs['object']
        context = super(ExpenseCategoryView, self).get_context_data(**kwargs)

        return context


class CurrencyAddView(AuthRequiredMixin, edit.CreateView):
    model = Currency
    form_class = CurrencyForm
    success_url = reverse_lazy('core:settings')

