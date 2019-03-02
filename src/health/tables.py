#!/usr/bin/python
# -*- coding: utf-8 -*-
# File:     health/tables.py
# Date:     2019-03-02 15:21
# Author:   Kenson Man <kenson@kenson.idv.hk>
# Desc:     Define the models for the health project;
from django_tables2 import Table, Column, A, TemplateColumn 
from webframe.CurrentUserMiddleware import get_current_request
from .models import *

class CategoriesTbl(Table):
   class Meta(object):
      model=Category
      attrs={'class': 'table'}
      row_attrs={ 'oId': lambda record: record.id }
      fields=('id', 'name', 'lmb', 'lmd')

