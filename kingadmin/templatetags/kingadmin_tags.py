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
    print(filter_obj)
    print("admin_class.filtered_list", admin_class.filtered_list)

    field_name = admin_class.model._meta.get_field(filter_obj)
    print(field_name)
    try:
        type_of_internal = field_name.get_internal_type()
        if type_of_internal in ('DateField','DateTimefield'):
            opt += "<select name=%s__gte>" %filter_obj
        else:
            opt += "<select name=%s>" %filter_obj
        for choice in field_name.get_choices():
            # print(filter_obj)
            # print(admin_class.filtered_list)
            # print(field_name.get_choices())
            # print(field_name.get_choices()[1])
            if filter_obj in admin_class.filtered_list:
                # print("admin_class.filtered_list",admin_class.filtered_list)
                # print("choice[0]",type(choice[0]))
                # print("admin_class.filtered_list.get(filter_obj)",type(admin_class.filtered_list.get(filter_obj)))
                if str(choice[0]) == admin_class.filtered_list.get(filter_obj):
                    opt += "<option selected value=%s>%s</option>" % (choice[0], choice[1])
                else:
                    opt += "<option value=%s>%s</option>" % (choice[0], choice[1])
            else:
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
                    month = ""
                    month = ("0"+ str(time_slot[0].month)) if time_slot[0].month < 10 else (str(time_slot[0].month))
                    # print(month)
                    day = ""
                    # print(str(time_slot[0].day))
                    day = ("0"+ str(time_slot[0].day)) if time_slot[0].day < 10 else (str(time_slot[0].day))
                    # print(time_slot[0].__format__("%Y-%m-%d"))
                    # print("time_slot[0].month-->>>",time_slot[0].month)
                    # print(admin_class.filtered_list["date__gte"])
                    # print("filter_obj+__gte-->>", filter_obj+"__gte")
                    if filter_obj+"__gte" in admin_class.filtered_list:
                        # print(admin_class.filtered_list[filter_obj+"__gte"])
                        print(time_slot[0].__format__("%Y-%m-%d"))
                        if admin_class.filtered_list[filter_obj+"__gte"] == time_slot[0].__format__("%Y-%m-%d"):
                            # print("yes?-->",admin_class.filtered_list[filter_obj+"__gte"])
                            opt += "<option selected value=%s-%s-%s>%s</option>" \
                                   % (year, month, day, time_slot[1])
                        # print("yes!!")
                        else:
                            opt += "<option value=%s-%s-%s>%s</option>" \
                                   % (year, month, day, time_slot[1])
                            # print("nonono")
                    else:
                        opt += "<option value=%s-%s-%s>%s</option>" \
                               % (year, month, day, time_slot[1])
                    # print(choice)
                else:
                    opt += "<option >------</option>"
            opt += "</select>"
    # print(opt)

    return mark_safe(opt)