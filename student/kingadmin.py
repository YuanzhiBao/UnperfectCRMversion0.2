#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'

from student import models
from kingadmin.sites import site

site.register(models.Student)
