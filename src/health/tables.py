#!/usr/bin/python
# -*- coding: utf-8 -*-
# File:     health/tables.py
# Date:     2019-03-02 15:21
# Author:   Kenson Man <kenson@kenson.idv.hk>
# Desc:     Define the models for the health project;
from django_tables2 import Table, Column, A, TemplateColumn 
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from pytz import timezone
from webframe.CurrentUserMiddleware import get_current_request
from webframe.models import Preference
from .models import *

class CategoriesTbl(Table):
   class Meta(object):
      model=Category
      attrs={'class': 'table'}
      row_attrs={ 'oId': lambda record: record.id }
      fields=('id', 'name', 'fmt', 'unit', 'lmb', 'lmd')

class IndexesTbl(Table):
   class Meta(object):
      model=Index
      attrs={'class': 'table'}
      row_attrs={ 'oId': lambda record: record.id, 'class':'row-data' }
      fields=('time', 'value', 'tagsString', 'desc')

   tagsString=Column(verbose_name=_('Index.tags'))
   value=Column(attrs={'style': 'text-align: right'})

   def render_time(self, value):
      if not hasattr(self, 'tz'):
         setattr(self, 'tz', timezone(settings.TIME_ZONE))
      return value.astimezone(self.tz).strftime(Preference.objects.pref('FMT_DATETIME', user=get_current_request().user, defval='%Y-%m-%d %H:%M', returnValue=True))

   def render_value(self, record, value):
      return record.category.fmt.format(value)
