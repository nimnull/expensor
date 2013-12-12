from django.contrib import admin
from .models import (Account, Person, Currency, ExpenseCategory,
    Transaction, Salary, Candidate, Inventory)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount',)
    readonly_fields = ('amount',)


class PersonSalaryInline(admin.StackedInline):
    model = Salary
    extra = 0


class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'is_active', 'salary',)
    list_filter = ('is_active', )
    inlines = [PersonSalaryInline]


class CandidateAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'title', 'status',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'bill_date', 'amount', 'amount_src', 'currency',
                    'direction', 'category',)
    list_filter = ('category', 'account', 'direction',)


class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'direct_expense', 'is_transfer')
    list_filter = ('direct_expense', 'is_transfer')


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'purchase_date', 'price', 
                    'inventory_type', 'person',)


admin.site.register(Account, AccountAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Currency)
admin.site.register(ExpenseCategory, ExpenseCategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Inventory, InventoryAdmin)

