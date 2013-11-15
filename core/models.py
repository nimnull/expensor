# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from datetime import datetime
from dateutil.relativedelta import relativedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
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
    last_review = models.DateField(blank=True, null=True)
    hospital = models.IntegerField(blank=True, null=True)

    objects = QuerySetManager()

    class Meta:
        ordering = ('first_name', 'last_name')

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
    def full_name(self):
        return u"{0.first_name} {0.last_name}".format(self)

    @property
    def vacation(self):       
        period = datetime.now().date() - self.works_from        
        return (period.days/30)*1.75

    @property
    def next_review(self):
        if self.last_review:
            return self.last_review + relativedelta(months=6)

    @property
    def salary(self):
        salaries = Salary.objects.filter(person=self,
                                         active_from__lte=datetime.now)
        if salaries.count() > 0:
            rv = salaries.latest('active_from')
        else:
            rv = Salary(amount=Decimal(0.00))
        return rv

    @property
    def salary_raise(self):
        salaries = Salary.objects.filter(person=self,
                                         active_from__lte=datetime.now)     
        if salaries.count() > 1:
            last = salaries[0].amount
            previous = salaries[1].amount
            rv = last-previous
        else:
            rv = 0
        return rv

  


division = (    
    ('1', 'QA'),
    ('2', 'Python'),
    ('3', 'JS'),
    ('4', 'Html/CSS'),
    ('5', 'Designer')
    )

status =  (    
    ('1', u'Отказали'),
    ('2', u'Сделали оффер/не принял'),
    ('3', u'Вышел на работу'),
    ('4', u'Бан-лист'),    
    )


class Candidate(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(db_index=True)
    phone = models.CharField(max_length=10)
    division = models.CharField(max_length=5, choices=division, blank=True, null=True)
    cv = models.URLField( blank=True, null=True)
    interview = models.URLField( blank=True, null=True)
    title = models.CharField(max_length=50,  blank=True, null=True)
    status = models.CharField(max_length=5, choices=status, blank=True, null=True)
    person = models.OneToOneField(Person, blank=True, null=True)

    objects = QuerySetManager()

    class Meta:
        ordering = ('first_name', 'last_name')


    class QuerySet(QuerySet):

        def qa(self):
            return self.filter(division='1')

        def python(self):
            return self.filter(division='2')

        def js(self):
            return self.filter(division='3')

        def html(self):
            return self.filter(division='4')

        def designer(self):
            return self.filter(division='5')            


    def __unicode__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('core:candidate', kwargs={'pk': self.pk})

    @property
    def full_name(self):
        return u"{0.first_name} {0.last_name}".format(self)





class Salary(models.Model):
    person = models.ForeignKey(Person, related_name='salaries')
    amount = models.DecimalField(u'сумма', decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(default=datetime.now)
    active_from = models.DateField(u'действует с', default=datetime.now)

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

    @property
    def balance(self):
        income = self.transactions.filter(direction=Transaction.DIRECTION_IN).\
            aggregate(Sum('amount'))['amount__sum'] or Decimal(0)
        expense = self.transactions.filter(direction=Transaction.DIRECTION_OUT).\
            aggregate(Sum('amount'))['amount__sum'] or Decimal(0)

        return income - expense


class ExpenseCategory(models.Model):
    name = models.CharField(u'название', max_length=255)
    direct_expense = models.BooleanField(u'прямой расход', default=True)
    is_transfer = models.BooleanField(u'перевод', default=False)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    @classmethod
    def get_commission(cls):
        return cls.objects.get(direct_expense=True, is_transfer=True)

    @classmethod
    def get_transfer(cls):
        return cls.objects.get(direct_expense=False, is_transfer=True)

    @classmethod
    def get_payment(cls):
        return cls.objects.get(direct_expense=False, is_transfer=False)

    def get_total(self):
        total = self.transactions.aggregate(Sum('amount'))['amount__sum']
        return total if total is not None else 0

class Currency(models.Model):
    name = models.CharField(u'название', max_length=255, unique=True)
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
    account = models.ForeignKey(Account, verbose_name=u'счёт',
                                related_name='transactions')
    category = models.ForeignKey(ExpenseCategory, verbose_name=u'тип',
                                 related_name='transactions',
                                 null=True, blank=True)
    person = models.ForeignKey(Person, verbose_name=u'сотрудник', null=True,
                               blank=True, related_name='transactions')
    parent = models.ForeignKey('self', verbose_name=u'связанная', null=True,
                               blank=True, related_name='children')
    currency = models.ForeignKey(Currency, verbose_name=u'валюта')

    direction = models.SmallIntegerField(choices=DIRECTION_CHOICES,
                                         db_index=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10,
                                 validators=[MinValueValidator(Decimal(0))])
    ratio = models.FloatField(u'коэффициент', default=1)
    amount_src = models.DecimalField(u'сумма', decimal_places=2, max_digits=10,
                                     validators=[MinValueValidator(Decimal(0))])
    bill_date = models.DateField(u'дата', default=datetime.now)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=True)

    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-bill_date',)

    def __unicode__(self):
        return "{0.id} {0.bill_date} {0.amount}".format(self)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.pk is None:
            self.set_amount(self.currency)
        return super(Transaction, self).save(force_insert, force_update, using,
                                             update_fields)

    def set_amount(self, currency):
        self.amount = Decimal(currency.ratio) * self.amount_src
        return self

    @classmethod
    def create_acceptor(cls, transaction, account):
        connected = cls.objects.create(
            amount_src=transaction.amount_src,
            ratio=transaction.ratio,
            account=account,
            direction=cls.DIRECTION_IN,
            created_by=transaction.created_by,
            category=transaction.category,
            currency=transaction.currency,
            bill_date=transaction.bill_date,
        )
        transaction.children.add(connected)
        return connected
