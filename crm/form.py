#!/usr/bin/evn python
# -*- coding:utf-8 -*-
__author__ = 'Yuanzhi Bao'

from django.forms import ModelForm
from crm import models
from django import forms


class CustomerInfoForm(ModelForm):
    class Meta:
        model = models.CustomerInfo
        fields = "__all__"
        exclude = ['consult_content','status']
        read_only = ['source','consultant','referral_name','contact_type']

    def __new__(cls, *args, **kwargs):
        print("cls.base_fields-->>", cls.base_fields)

        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class':'form-control'})

        for field_name in cls.Meta.read_only:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'disabled': 'true'})

        return ModelForm.__new__(cls)

    def clean(self):
        print("cleaned_data-->", self.cleaned_data)

        if self.errors:
            raise forms.ValidationError(("Please fix errors before resubmit."))
        if self.instance.id is not None:
            for field in self.Meta.read_only:
                old_field_val = getattr(self.instance, field)
                form_val = self.cleaned_data.get(field)
                print("两个不同的值", old_field_val, form_val)
                if old_field_val != form_val:
                    self.add_error(field, "Readonly Field: field should be '{value}' ,not '{new_value}' ". \
                                   format(**{'value': old_field_val, 'new_value': form_val}))





