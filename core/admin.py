from django.contrib import admin
from .models import Account, Person, Currency, ExpenseCategory, Transaction


class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount')
    readonly_fields = ('amount',)


class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'is_active', 'salary')
    list_filter = ('is_active', )

admin.site.register(Account, AccountAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Currency)
admin.site.register(ExpenseCategory)
admin.site.register(Transaction)
