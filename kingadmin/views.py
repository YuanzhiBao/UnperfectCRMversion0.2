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
    if need_sort_column_index:
        need_sort_column_name = admin_class.list_display[int(need_sort_column_index)]
        # print(querysets)
        querysets = querysets.order_by(need_sort_column_name)
        # print(querysets)
        return need_sort_column_name,querysets
    else:
        return None,querysets


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
    need_sort_column_name,sorted_querysets = sorted_querysets_by_column(request, querysets, admin_class)
    querysets  = Paginator(sorted_querysets ,2)
    page = request.GET.get('page')
    try:
        querysets = querysets.get_page(page)
    except PageNotAnInteger:
        querysets = querysets.get_page(1)
    except EmptyPage:
        querysets = querysets.get_page(querysets.num_pages)



    # print(filtered_list)

    return render(request, "kingadmin/table_list.html",\
                  {"querysets": querysets,"model_name":model_name,"admin_class":admin_class})
