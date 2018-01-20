#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'

from student import models
from kingadmin.sites import site
from kingadmin.admin_base import BaseKingAdmin



class CustomerAdmin(BaseKingAdmin):
    list_display = ['name']

site.register(models.Student,CustomerAdmin)
