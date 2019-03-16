#!/usr/bin/python
# -*- coding: utf-8 -*-
# File:     health/views.py
# Date:     2019-03-02 13:30
# Author:   Kenson Man <kenson@kenson.idv.hk>
# Desc:     Define the models for the health project;
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Min, Max, Avg, Count
from django.shortcuts import render, redirect, get_object_or_404 as getObj
from django.utils.translation import gettext_lazy as _
from django_tables2.config import RequestConfig
from webframe.functions import FMT_DATETIME, getDateTime
from webframe.models import Preference
from .tables import *
import logging

logger=logging.getLogger('health.views')

# Create your views here.
@login_required
def dashboard(req):
   params=dict()
   params['target']=Category.objects.filter(user=req.user).order_by('sequence')
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
   if not target.isNew():
      if target.user != req.user: raise PermissionDenied()

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
      target.fmt=req.POST.get('fmt', None)
      target.sequence=float(req.POST.get('sequence', '100'))
      target.unit=req.POST.get('unit', None)
      target.user=req.user
      target.save()

      ntags=[t.strip() for t in req.POST.get('tags', '').split(',') if len(t.strip())>0]
      otags=[t.name for t in Tag.objects.filter(category=target)]
      for t in ntags:
         if t not in otags: Tag(category=target, name=t).save() # Create the new tag if that is not exists in otags
      for t in otags:
         if t not in ntags: Tag.objects.get(category=target, name=t).delete() #Remove the tag if that is not exists in ntags
      messages.success(req, _('%(objtype)s::%(target)s[%(id)s] saved')%{'objtype': _('health.models.Category'), 'target':target.name, 'id':target.id})
      return redirect('categories')
   elif req.method=='DELETE':
      if not req.user.has_perm('health.delete_category'): raise PermissionDenied()
      target.delete()
      messages.warning(req, _('%(objtype)s::%(target)s[%(id)s] deleted')%{'objtype': _('health.models.Category'), 'target':target.name, 'id':target.id})
      return redirect('categories')

   params['target']=target
   return render(req, 'health/category.html', params)

@login_required
@transaction.atomic
def widget(req, id):
   params=dict()
   target=Category() if id=='new' else getObj(Category, id=id)
   if not target.isNew():
      if target.user != req.user: raise PermissionDenied()

   if req.method=='POST':
      if not req.user.has_perm('health.add_index'): raise PermissionDenied()
      if req.user != target.user: raise PermissionDenied('Cannot cross category/user')
      index=Index()
      index.category=target
      index.time=getDateTime(req.POST.get('time', None), None, req.POST.get('FMT_DATETIME', FMT_DATETIME))
      index.value=float(req.POST.get('value', '0.0'))
      index.desc=req.POST.get('desc', None)
      index.save()
      for t in req.POST.get('tags', '').split(','):
         if len(t.strip())<1: continue
         t=Tag.objects.get(category=target, name=t.strip())
         index.tags.add(t)
      return redirect('dashboard')
   elif req.method=='GET':
      filter=[f.strip() for f in req.GET.get('filter', '').split(',') if len(f.strip()) > 0]
      df=req.GET.get('FMT_DATETIME', FMT_DATETIME)
      startDate=getDateTime(req.GET.get('form', None), None, df)
      endDate=getDateTime(req.GET.get('to', None), None, df)
      page=int(req.GET.get('page', '1'))
      pageSize=int(Preference.objects.pref('PAGE_SIZE', defval=10, user=req.user, returnValue=True))
      params['data']=Index.objects.filter(category=target).order_by('-time')
      for f in filter: 
         logger.info('Atemp filter: %s'%f)
         params['data']=params['data'].filter(tags__in=Tag.objects.filter(name=f))
      if startDate: params['data']=params['data'].filter(time__gte=startDate)
      if endDate: params['data']=params['data'].filter(time__lte=endDate)
      params['info']=params['data'].aggregate(avg=Avg('value'), max=Max('value'), min=Min('value'), count=Count('value'))
      params['target']=target
      params['indexes']=Paginator(params['data'], pageSize).page(page)
      params['table']=IndexesTbl(params['data'])
      params['filter']=', '.join(filter)
      params['form']=startDate
      params['to']=endDate
      RequestConfig(req, paginate={'per_page': pageSize}).configure(params['table'])
      return render(req, 'health/widget.html', params)
