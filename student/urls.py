#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'

from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from student import views

urlpatterns = [
    url(r'^$', views.student_index),
]