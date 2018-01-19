#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'

from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from kingadmin import views

urlpatterns = [
    url(r'^signin/',views.signin,name="signin"),
    url(r'^signout/',views.signout,name="signout"),
    url(r'^$', views.king_admin_index,name="king_admin_index"),
]