#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'
from django import conf
import importlib

def discover():
    print("--->>discover conf.settings.INSTALLED_APPS",conf.settings.INSTALLED_APPS)
    apps = conf.settings.INSTALLED_APPS
    for app_name in apps:
        try:
            app_imported = importlib.__import__("%s.kingadmin" %app_name)
            print("--->>discover app_imported", app_imported)
        except ModuleNotFoundError:
            pass
