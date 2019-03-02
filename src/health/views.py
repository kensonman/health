#!/usr/bin/python
# -*- coding: utf-8 -*-
# File:     health/views.py
# Date:     2019-03-02 13:30
# Author:   Kenson Man <kenson@kenson.idv.hk>
# Desc:     Define the models for the health project;
from django.shortcuts import render

# Create your views here.
def dashboard(req):
   params=dict()
   return render(req, 'health/dashboard.html', params)
