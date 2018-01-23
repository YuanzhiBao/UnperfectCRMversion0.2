#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'

from django.template import Library

from django.utils.safestring import mark_safe

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
    field_name = admin_class.model._meta.get_field(filter_obj)
    try:
        opt += "<select>"
        for choice in field_name.get_choices():
            opt += "<option>%s - %s</option>" % choice
            print(choice)
        opt += "</select>"
    except AttributeError:
        pass
    # print(opt)

    return mark_safe(opt)