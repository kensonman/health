#!/usr/bin/python
# -*- coding: utf-8 -*-
# Date:     2019-03-02 13:30
# Author:   Kenson Man <kenson@kenson.idv.hk>
# Desc:     Define the models for the health project;
from django.db import models, transaction
from django.conf import settings
from django.utils import timezone as tz
from django.utils.translation import gettext_lazy as _
from webframe.models import ValueObject, OrderableValueObject, AliveObject, AliveObjectManager
import logging

logger=logging.getLogger('health.models')
maxval=8 #Max-Digits
decval=5 #Decimal-Places
defval=0 #Default-Value

class Category(OrderableValueObject):
   class META(object):
      verbose_name         =_('health.models.Category')
      verbose_name_plural  =_('health.models.Categories')

   name                    =models.CharField(max_length=100, verbose_name=_('Category.name'))
   desc                    =models.TextField(max_length=4096, null=True, blank=True, verbose_name=_('Category.desc'))
   minimum                 =models.DecimalField(max_digits=maxval, decimal_places=decval, default=defval, verbose_name=_('Category.minimum'))
   maximum                 =models.DecimalField(max_digits=maxval, decimal_places=decval, default=defval, verbose_name=_('Category.maximum'))
   user                    =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Category.user'))

   @property
   def tags(self):
      return Tag.objects.filter(category=self).order_by('name')

   @property
   def tagsString(self):
      return ', '.join([t.name for t in self.tags])

class Tag(ValueObject):
   class META(object):
      verbose_name         =_('health.models.Tag')
      verbose_name_plural  =_('health.models.Tags')

   category                =models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name=_('Tag.category'))
   name                    =models.CharField(max_length=100, verbose_name=_('Tag.name'))

class Index(ValueObject):
   class META(object):
      verbose_name         =_('health.models.Index')
      verbose_name_plural  =_('health.models.Indexes')

   time                    =models.DateTimeField(default=tz.now, verbose_name=('Index.time'))
   category                =models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name=_('Index.category'))
   value                   =models.DecimalField(max_digits=maxval, decimal_places=decval, default=defval, verbose_name=_('Index.value'))
   tags                    =models.ManyToManyField(Tag, verbose_name=_('Index.tags'))
