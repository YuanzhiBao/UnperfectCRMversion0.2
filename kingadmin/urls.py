#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'

from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from kingadmin import views

urlpatterns = [
    url(r'^$', views.king_admin_index, name="king_admin_index"),
    url(r'^(\w+)/(\w+)/$', views.table_list, name="table_list"),
    url(r'^signin/',views.signin,name="signin"),
    url(r'^signout/',views.signout,name="signout"),
]