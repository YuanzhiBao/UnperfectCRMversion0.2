#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'

from django.shortcuts import render, redirect


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
        return redirect("/kingadmin/")


