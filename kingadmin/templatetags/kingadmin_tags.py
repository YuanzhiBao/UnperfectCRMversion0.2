#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'

from django.template import Library

from django.utils.safestring import mark_safe

import datetime,time

register = Library()



@register.simple_tag
def build_table_row(obj, admin_class):
    ele = ""
    for column_name in admin_class.list_display:
        column_obj = admin_class.model._meta.get_field(column_name)
        if column_obj.choices:
            column_data = getattr(obj, "get_%s_display" %column_name)()
        else:
            column_data = getattr(obj, column_name)
        ele += "<td>%s</td>" % column_data

    return mark_safe(ele)


@register.simple_tag
def build_filter_row(filter_obj, admin_class):
    opt = ""
    # print(filter_list)
    # print(filter_obj)
    field_name = admin_class.model._meta.get_field(filter_obj)
    try:
        type_of_internal = field_name.get_internal_type()
        if type_of_internal in ('DateField','DateTimefield'):
            opt += "<select name=%s__gte>" %filter_obj
        else:
            opt += "<select name=%s>" %filter_obj
        for choice in field_name.get_choices():
            opt += "<option value=%s>%s</option>" % (choice[0], choice[1])
            # print(choice)
        opt += "</select>"
    except AttributeError:
        type_of_internal = field_name.get_internal_type()
        # print(type_of_internal)
        if type_of_internal in ('DateField','DateTimefield'):
            now_time = datetime.datetime.now()
            time_opt_list = [
                ('', "-------"),
                ( now_time,"Today"),
                ( now_time - datetime.timedelta(7),"7 Days Ago"),
                ( now_time.replace(day=1),"This month"),
                ( now_time - datetime.timedelta(90),"Within Three month"),
                ( now_time.replace(month=1,day=1),"This Year"),
            ]
            for time_slot in time_opt_list:
                # print(type(time_slot[1]))
                if time_slot[0] != "":
                    year = str(time_slot[0].year)
                    month = str(time_slot[0].month)
                    day = str(time_slot[0].day)
                    opt += "<option value=%s-%s-%s>%s</option>" \
                           % (time_slot[0].year, time_slot[0].month, time_slot[0].day, time_slot[1])
                    # print(choice)
                else:
                    opt += "<option >------</option>"
            opt += "</select>"
    # print(opt)

    return mark_safe(opt)