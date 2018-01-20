#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'
# For every model which register in kingadmin
# set up a global dic to represents the data
# in a formatal way

from kingadmin.admin_base import BaseKingAdmin


class AdminSite(object):
    def __init__(self):
        self.enabled_admin = {}

    def register(self, model_class, admin_class=None):
        # print("--->>AdminSite model_class",model_class._meta.app_label)
        # print("--->>AdminSite model_class",model_class._meta.model_name)
        app_label = model_class._meta.app_label
        model_name = model_class._meta.model_name
        if not admin_class:
            admin_class = BaseKingAdmin() #为了避免多个model共享同一个BaseKingAdmin
        else:
            admin_class = admin_class()

        admin_class.model = model_class
        if app_label not in self.enabled_admin:
            self.enabled_admin[app_label] = {}

        self.enabled_admin[app_label][model_name] = admin_class
        # admin_class.model = model_name
        # print(model_class.objects.all())
        # print("--->>AdminSite model_class", self.enabled_admin)

site = AdminSite()
