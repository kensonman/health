#!/usr/bin/python
# -*- coding: utf-8 -*-
# File:     health/views.py
# Date:     2019-03-02 13:30
# Author:   Kenson Man <kenson@kenson.idv.hk>
# Desc:     Define the models for the health project;
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404 as getObj
from .tables import *
import logging

logger=logging.getLogger('health.views')

# Create your views here.
def dashboard(req):
   params=dict()
   return render(req, 'health/dashboard.html', params)

# Showing the Categories
@login_required
def categories(req):
   params=dict()
   params['target']=CategoriesTbl(Category.objects.filter(user=req.user))
   return render(req, 'health/categories.html', params)

@login_required
def category(req, id):
   params=dict()
   target=Category() if id=='new' else getObj(Category, id=id)

   params['target']=target
   return render(req, 'health/category.html', params)
