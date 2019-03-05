"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from webframe.urls import urlpatterns as webframe
from . import views


urlpatterns = [
    re_path('^$', views.dashboard, name='dashboard'),
    re_path('^categories/?$', views.categories, name='categories'),
    re_path('^categories/(?P<id>[^\/]+)/?$', views.category, name='category'),
    re_path('^categories/(?P<id>[^\/]+)/widget/?$', views.widget, name='widget'),
]
