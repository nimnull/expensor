from decimal import Decimal
from django import template
from core.models import Currency

register = template.Library()


@register.filter
def currency(value, currency_name):
    """Calculating and formating amount in specific currency"""
    try:
        currency_obj = Currency.objects.get(name=currency_name)
    except Currency.DoesNotExist:
        return value
    value = value / Decimal(currency_obj.ratio)
    return u"%0.2f %s" % (value, currency_name)