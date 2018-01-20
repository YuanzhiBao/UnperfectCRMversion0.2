#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'
# For every model which register in kingadmin
# set up a global dic to represents the data
# in a formatal way


class AdminSite(object):
    def __init__(self):
        self.enabled_admin = {}

    def register(self, model_class, admin_class=None):
        # print("--->>AdminSite model_class",model_class._meta.app_label)
        # print("--->>AdminSite model_class",model_class._meta.model_name)
        app_label = model_class._meta.app_label
        model_name = model_class._meta.model_name
        if app_label not in self.enabled_admin:
            self.enabled_admin[app_label] = {}
        self.enabled_admin[app_label][model_name] = admin_class
        # print("--->>AdminSite model_class", self.enabled_admin)

site = AdminSite()