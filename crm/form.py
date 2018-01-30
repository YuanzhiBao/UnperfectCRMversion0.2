#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'

from django.forms import ModelForm
from crm import models


class CustomerInfo(ModelForm):
    class Meta:
        model = models.CustomerInfo
        fields = "__all__"

    def __new__(cls, *args, **kwargs):
        print("cls.base_fields-->>", cls.base_fields)

        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class':'form-control'})

        return ModelForm.__new__(cls)



