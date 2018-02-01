#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'

from django.shortcuts import render, redirect

from kingadmin import sites

class BaseKingAdmin(object):
    list_display = []
    list_filter = []
    search_fields = []
    list_per_page = 25
    readonly_fields =[]
    defualt_actions = ['delete_all',]
    actions = []

    def __init__(self):
        self.actions.extend(self.defualt_actions)

    def delete_all(self, request, querysets):
        #这里的self就是admin_class
        #在sites里面为不同的model注册了admin_class 代码如下

                    # if not admin_class:
                    #     admin_class = BaseKingAdmin()  # 为了避免多个model共享同一个BaseKingAdmin
                    # else:
                    #     admin_class = admin_class()

        print(self)
        # sites.site.enabled_admin
        # admin_class = site.enabled_admin[app_name][model_name]
        print("request-->",request)
        print("request.POST-->",request.POST)
        print("request_model_name", request.POST.get("model_name"))
        # return render(request, "kingadmin/table_obj_delete.html")


