#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'
from django.core.paginator import Paginator,PageNotAnInteger
from crm import models
from kingadmin.sites import site
from kingadmin.admin_base import BaseKingAdmin
from django.shortcuts import render, redirect

class CustomerAdmin(BaseKingAdmin):
    list_display = ['id','name','source','contact_type','consultant','referral_name','status','date',]
    list_filter = ['source','consultant', 'date']
    search_fields = ['name', 'contact', 'consultant__name']
    readonly_fields = ['status', 'consultant',]
    filter_horizontal = ['consult_courses', ]
    list_per_page = 10
    actions = ["duang",]



    def duang(self, request, querysets):
        querysets.update(status=0)
        return redirect("/kingadmin/")


site.register(models.UserProfile)
site.register(models.CustomerInfo,CustomerAdmin)
site.register(models.CustomerFollowUp)
site.register(models.Course)
site.register(models.ClassList)
site.register(models.Branch)
site.register(models.Role)
site.register(models.StudyRecord)
site.register(models.Student)
site.register(models.Menus)

# Register your models here.


