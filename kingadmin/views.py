from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django import conf
import importlib
from kingadmin.sites import site
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage

# print("kingadmin\\views.py", site.enabled_admin)


# Create your views here.

def signin(request):
    print(request.GET.get)
    print(request.POST.get)
    print(request.method)
    if request.method == "POST":
        # return redirect("/crm/")
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username)
        print(password)

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
        if key in ("page","o"):continue
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



@login_required
def table_list(request, app_name, model_name):
    # print(site.enabled_admin[app_name][model_name].model.objects.all())

    admin_class = site.enabled_admin[app_name][model_name] #get the admin_class class save in the list
    querysets = admin_class.model.objects.all() # get the data

    # print(request.GET)
    filter_list = request.GET
    #get the selected_set and render them in front-end
    filtered_query, querysets = selected_set(filter_list, querysets)
    admin_class.filtered_query = filtered_query

    #avoid get the warning that Paginotor could get unpredicatetabl result for unordered queryset
    querysets = querysets.order_by('id')

    need_sort_column_name,sorted_querysets, sorted_column = sorted_querysets_by_column(request, querysets, admin_class)
    # print(need_sort_column_name)
    querysets  = Paginator(sorted_querysets ,4)
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

    return render(request, "kingadmin/table_list.html",\
                  {"querysets": querysets,"model_name":model_name,\
                   "admin_class":admin_class, "need_sort_column_name": need_sort_column_name})
