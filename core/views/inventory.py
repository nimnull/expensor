from django.views.generic import ListView, DetailView, edit
from core.forms import InventoryForm
from core.models import Inventory
from core.views.base import AuthRequiredMixin



class InventoryView(AuthRequiredMixin, ListView):
    model = Inventory

    def get_context_data(self, **kwargs):
        context = super(InventoryView, self).get_context_data(**kwargs)
        context['inventory_form'] = InventoryForm()
        return context


class InventoryItemView(DetailView):
    model = Inventory

    def get_context_data(self, **kwargs):
        inventory = kwargs['object']
        context = super(InventoryItemView, self).get_context_data(**kwargs)
        context['inventory_form'] = InventoryForm(instance=inventory)
        return context


class InventoryAdd(AuthRequiredMixin, edit.CreateView):
    model = Inventory
    form_class = InventoryForm


class InventoryEdit(AuthRequiredMixin, edit.UpdateView):
    model = Inventory
    form_class = InventoryForm