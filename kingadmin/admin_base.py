#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'

from django.shortcuts import render, redirect

from kingadmin import sites


import json

class BaseKingAdmin(object):
    list_display = []
    list_filter = []
    search_fields = []
    list_per_page = 25
    readonly_fields =[]
    default_actions = ['delete_all']
    actions = []

    def __init__(self):
        self.actions.extend(self.default_actions)

    def delete_all(self, request, querysets):
        #这里的self就是admin_class
        #在sites里面为不同的model注册了admin_class 代码如下

                    # if not admin_class:
                    #     admin_class = BaseKingAdmin()  # 为了避免多个model共享同一个BaseKingAdmin
                    # else:
                    #     admin_class = admin_class()

        # print(querysets)
        # print("type(querysets)-->",type(querysets))
        querysets_ids = json.dumps([i.id for i in querysets])
        print("self.aqq_name-->",self.model._meta.app_label)


        return render(request, "kingadmin/table_obj_delete.html", \
                      {"admin_class":self, "objs": querysets,'querysets_ids':querysets_ids,\
                       'app_name':self.model._meta.app_label,'model_name':self.model._meta.model_name})


        # return render(request, "kingadmin/table_obj_delete.html")


