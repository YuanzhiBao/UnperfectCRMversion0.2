#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'

from crm import models
from kingadmin.sites import site

site.register(models.UserProfile)
site.register(models.Student)
site.register(models.Menus)

