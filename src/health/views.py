#!/usr/bin/python
# -*- coding: utf-8 -*-
# File:     health/views.py
# Date:     2019-03-02 13:30
# Author:   Kenson Man <kenson@kenson.idv.hk>
# Desc:     Define the models for the health project;
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404 as getObj
from django.utils.translation import gettext_lazy as _
from .tables import *
import logging

logger=logging.getLogger('health.views')

# Create your views here.
@login_required
def dashboard(req):
   params=dict()
   params['target']=CategoriesTbl(Category.objects.filter(user=req.user).order_by('sequence'))
   return render(req, 'health/dashboard.html', params)

# Showing the Categories
@login_required
def categories(req):
   params=dict()
   params['target']=CategoriesTbl(Category.objects.filter(user=req.user).order_by('sequence'))
   return render(req, 'health/categories.html', params)

@login_required
@transaction.atomic
def category(req, id):
   params=dict()
   target=Category() if id=='new' else getObj(Category, id=id)

   if req.method=='POST' or req.method=='PUT':
      #Check permission
      if target.isNew():
         if not req.user.has_perm('health.add_category'): raise PermissionDenied()
      else:
         if not req.user.has_perm('health.change_category'): raise PermissionDenied()

      target.name=req.POST.get('name', None)
      target.desc=req.POST.get('desc', None)
      target.minimum=Decimal(req.POST.get('minimum', '0'))
      target.maximum=Decimal(req.POST.get('maximum', '0'))
      target.sequence=float(req.POST.get('sequence', '100'))
      target.user=req.user
      target.save()
      messages.success(req, _('%(objtype)s::%(target)s[%(id)s] saved')%{'objtype': _('health.models.Category'), 'target':target.name, 'id':target.id})
      return redirect('categories')
   elif req.method=='DELETE':
      if not req.user.has_perm('health.delete_category'): raise PermissionDenied()
      target.delete()
      messages.warning(req, _('%(objtype)s::%(target)s[%(id)s] deleted')%{'objtype': _('health.models.Category'), 'target':target.name, 'id':target.id})
      return redirect('categories')

   params['target']=target
   return render(req, 'health/category.html', params)
