from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
import json
from kingadmin import form_handler
from kingadmin.sites import site


# print("kingadmin\\views.py", site.enabled_admin)


# Create your views here.

def signin(request):
    # print(request.GET.get)
    # print(request.POST.get)
    # print(request.method)
    if request.method == "POST":
        # return redirect("/crm/")
        username = request.POST.get("username")
        password = request.POST.get("password")
        # print(username)
        # print(password)

        user = authenticate(username=username, password=password)
        # print(request.GET.get('next'))
        # print(request.GET.get)
        if user:
            login(request,user)
            return redirect(request.GET.get('next','king_admin_index'))
        else:
            return render(request, "kingadmin/signin.html",{"error_msg": "wrongwrong!"})
    else:
        return render(request, "kingadmin/signin.html")


def signout(request):
    logout(request)
    return redirect('/signin/')


def king_admin_index(request):
    return render(request, "kingadmin/king_admin_index.html",{"sites": site.enabled_admin})


def selected_set(filter_list, querysets):
    filtered_list = {}
    for key,value in filter_list.items():
        if key in ("page","o","search_fileds"):continue
        if value == "---------":
            filtered_list[key] = "1970-07-01"
        elif value:
            filtered_list[key] = value
        # if value:
        #     filtered_list[key] = value
        #     if value == "---------":
        #         filtered_list[key] = "1970-07-01"
    return filtered_list, querysets.filter(**filtered_list)


def sorted_querysets_by_column(request, querysets, admin_class):
    need_sort_column_index = request.GET.get('o')
    sorted_column = {}
    if not need_sort_column_index:
        return None, querysets, sorted_column
    elif need_sort_column_index.startswith('-'):
        need_sort_column_name = admin_class.list_display[abs(int(need_sort_column_index))]
        # print(querysets)
        need_sort_column_name = '-'+ need_sort_column_name
        querysets = querysets.order_by(need_sort_column_name)
        sorted_column[need_sort_column_name.strip('-')] = str(abs(int(need_sort_column_index)))
        # print(sorted_column)
        return need_sort_column_name,querysets, sorted_column
    else:
        need_sort_column_name = admin_class.list_display[abs(int(need_sort_column_index))]
        querysets = querysets.order_by(need_sort_column_name)
        sorted_column[need_sort_column_name.strip('-')] = '-' + need_sort_column_index
        # print(sorted_column)
        return need_sort_column_name, querysets, sorted_column



def searched_querysets(request, sorted_querysets, admin_class):
    search_demand = request.GET.get("search_fileds")
    # print(search_demand)
    if search_demand:
        q = Q()
        q.connector = 'OR'
        for search_filed in admin_class.search_fields:
            q.children.append(("%s__contains" % search_filed, search_demand))

        return sorted_querysets.filter(q)
    return sorted_querysets




@login_required
def table_list(request, app_name, model_name):
    # print(site.enabled_admin[app_name][model_name].model.objects.all())

    admin_class = site.enabled_admin[app_name][model_name] #get the admin_class class save in the list


    if request.method == "POST":
        selected_obj_action = request.POST.get("action")
        selected_ids = json.loads(request.POST.get('selected_ids'))
        print("selected_ids in admin", selected_ids)

        if not selected_obj_action and selected_ids:
            print("dwaddaw--->>",admin_class.model.objects.filter(id__in=selected_ids))
            selected_objs = admin_class.model.objects.filter(id__in=selected_ids).delete()
            # selected_objs.delete()
        else:
            selected_objs = admin_class.model.objects.filter(id__in=selected_ids)
            admin_class_func = getattr(admin_class, selected_obj_action)
            print("admin_class_func-->>",admin_class_func)
            response = admin_class_func(request, selected_objs)
            if response:
                return response


    querysets = admin_class.model.objects.all().order_by('-id')# get the data

    # print(request.GET)
    # print("dir--->>>>",dir(querysets))
    filter_list = request.GET
    #get the selected_set and render them in front-end
    filtered_query, querysets = selected_set(filter_list, querysets)
    admin_class.filtered_query = filtered_query

    #avoid get the warning that Paginotor could get unpredicatetabl result for unordered queryset
    querysets = querysets.order_by('-id')

    need_sort_column_name,sorted_querysets, sorted_column = sorted_querysets_by_column(request, querysets, admin_class)
    # print(need_sort_column_name)

    searched_queryset = searched_querysets(request, sorted_querysets, admin_class)

    querysets  = Paginator(searched_queryset ,admin_class.list_per_page)
    page = request.GET.get('page')
    try:
        querysets = querysets.get_page(page)
    except PageNotAnInteger:
        querysets = querysets.get_page(1)
    except EmptyPage:
        querysets = querysets.get_page(querysets.num_pages)




    admin_class.sorted_colunm_name = need_sort_column_name


    #sorted_column 是sort一句的那个个列  返回形式如：{"name":"-1"}或是 {'consultant': '-4'}
    admin_class.sorted_column = sorted_column
    # print(filtered_list)

    return render(request, "kingadmin/table_list.html",locals())


def table_obj_change(request, app_name, model_name, obj_id):
    admin_class = site.enabled_admin[app_name][model_name]  # get the admin_class class save in the list
    # querysets = admin_class.model.objects.all()  # get the data
    obj = admin_class.model.objects.get(id=obj_id)

    model_form = form_handler.get_dynamic_modelform(admin_class)

    if request.method == "GET":
        form_obj = model_form(instance=obj)
    elif request.method == "POST":
        form_obj = model_form(instance=obj, data=request.POST)
        # print("POST:-->>>", form_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/kingadmin/%s/%s/" %(app_name,model_name))

    # print(form_obj.instance)

    # from crm import models
    #
    # from crm import form
    #
    # form_obj = form.CustomerInfo()

    return render(request, "kingadmin/table_obj_change.html", locals())


def table_obj_add(request, app_name, model_name):
    admin_class = site.enabled_admin[app_name][model_name]  # get the admin_class class save in the list
    # querysets = admin_class.model.objects.all()  # get the data

    model_form = form_handler.get_dynamic_modelform(admin_class, True)

    admin_class.add_form_bool = True

    if request.method == "GET":
        form_obj = model_form()
    elif request.method == "POST":
        form_obj = model_form(data=request.POST)
        # print("POST:-->>>", form_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/kingadmin/%s/%s/" % (app_name, model_name))

    return render(request, "kingadmin/table_obj_add.html", locals())


@login_required
def table_obj_delete(request, app_name, model_name, obj_id):
    admin_class = site.enabled_admin[app_name][model_name]
    obj = admin_class.model.objects.get(id=obj_id)


    if request.method == "POST":
        obj.delete()
        return redirect("/kingadmin/{app_name}/{model_name}/".format(app_name=app_name,model_name=model_name))

    return render(request, "kingadmin/table_obj_delete.html", locals())