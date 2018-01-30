#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'

from django.forms import ModelForm


def get_dynamic_modelform(admin_class, add_form_bool = False):

    class Meta:
        model = admin_class.model
        fields = "__all__"
        if not add_form_bool:
            exclude = admin_class.readonly_fields
            admin_class.add_form_bool = False

    def __new__(cls, *args, **kwargs):
        # print("cls.base_fields-->>", cls.base_fields)

        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class':'form-control'})

        return ModelForm.__new__(cls)

    form_obj = type("get_dynamic_modelform", (ModelForm,), {"Meta": Meta,'__new__': __new__})

    return form_obj


