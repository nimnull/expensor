# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from . import DIRECTION_CHOICES


class Transaction(models.Model):
    direction = models.SmallIntegerField(choices=DIRECTION_CHOICES,
                                         db_index=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10,
                                 validators=[MinValueValidator(Decimal(0))])
