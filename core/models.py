# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from datetime import datetime
from decimal import Decimal
from django.contrib.auth.models import User
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.query import QuerySet

from .managers import QuerySetManager


class Action(models.Model):
    name = models.CharField(max_length=128)


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(db_index=True)
    phone = models.CharField(max_length=10)
    position = models.CharField(max_length=256)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(db_index=True, default=False)
    works_from = models.DateField(default=datetime.now)

    objects = QuerySetManager()

    class QuerySet(QuerySet):

        def active(self):
            return self.filter(is_active=True)

        def inactive(self):
            return self.filter(is_active=False)

    def __unicode__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('core:person', kwargs={'pk': self.pk})

    @property
    def salary(self):
        return Salary.objects.filter(person=self, active_from__lte=datetime.now).latest('active_from')

    @property
    def full_name(self):
        return u"{0.first_name} {0.last_name}".format(self)


class Salary(models.Model):
    person = models.ForeignKey(Person, related_name='salaries')
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(default=datetime.now)
    active_from = models.DateField(default=datetime.now)

    objects = QuerySetManager()

    class Meta:
        # get_latest_by = '-active_from'
        ordering = ('-active_from', )

    class QuerySet(QuerySet):

        def active(self):
            return self.filter(active_from__lte=datetime.now).latest()

    def __unicode__(self):
        return self.amount

    def get_absolute_url(self):
        return reverse('core:person', kwargs={'pk': self.person.pk})


class Account(models.Model):
    name = models.CharField(u'название', max_length=255)
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    comment = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name


class ExpenseCategory(models.Model):
    name = models.CharField(u'название', max_length=255)

    def __unicode__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(u'название', max_length=255)
    ratio = models.FloatField(u'коэффициент', default=1)
    is_default = models.BooleanField(u'системная?', default=False)

    class Meta:
        verbose_name_plural = 'currencies'

    def __unicode__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.is_default:
            Currency.objects.filter(is_default=True).update(is_default=False)

        super(Currency, self).save(force_insert, force_update, using,
                                   update_fields)

    @classmethod
    def default(cls):
        return cls.objects.get(is_default=True)


class Transaction(models.Model):

    DIRECTION_IN = 1
    DIRECTION_OUT = 2

    DIRECTION_CHOICES = (
        (DIRECTION_IN, u'приход'),
        (DIRECTION_OUT, u'расход')
    )

    created_by = models.ForeignKey(User)
    source = models.ForeignKey(Account, verbose_name=u'счёт')
    category = models.ForeignKey(ExpenseCategory, verbose_name=u'тип',
                                 null=True, blank=True)
    person = models.ForeignKey(Person, verbose_name=u'сотрудник', null=True,
                               blank=True)

    direction = models.SmallIntegerField(choices=DIRECTION_CHOICES,
                                         db_index=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10,
                                 validators=[MinValueValidator(Decimal(0))])
    ratio = models.FloatField(u'коэффициент', default=1)
    amount_src = models.DecimalField(decimal_places=2, max_digits=10,
                                     validators=[MinValueValidator(Decimal(0))])
    bill_date = models.DateField(u'дата', default=datetime.now)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=True)

    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-bill_date',)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.amount = Decimal(self.ratio) * self.amount_src
        return super(Transaction, self).save(force_insert, force_update, using,
                                             update_fields)
