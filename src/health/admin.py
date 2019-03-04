#!/usr/bin/python
# -*- coding: utf-8 -*-
# File:     health/admin.py
# Date:     2019-03-04 20:52
# Author:   Kenson Man <kenson@kenson.idv.hk>
# Desc:     Define the admin-tools for the health project;
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
   list_display=('id', 'name', 'desc', 'fmt', 'minimum', 'maximum', 'user', 'lmb', 'lmd')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
   list_display=('id', 'category_user',  'category_name', 'name', 'lmb', 'lmd')

   def category_user(self, record):
      return record.category.user
   category_user.short_description=_('Category.user')

   def category_name(self, record):
      return record.category.name
   category_name.short_description=_('Category.name')

@admin.register(Index)
class IndexAdmin(admin.ModelAdmin):
   list_display=('id', 'category_user',  'category_name', 'value', 'lmb', 'lmd')

   def category_user(self, record):
      return record.category.user
   category_user.short_description=_('Category.user')

   def category_name(self, record):
      return record.category.name
   category_name.short_description=_('Category.name')
   
