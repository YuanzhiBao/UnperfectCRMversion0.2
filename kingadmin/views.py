from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django import conf
import importlib
from kingadmin.sites import site

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


@login_required
def table_list(request, app_name, model_name):
    # print(site.enabled_admin[app_name][model_name].model.objects.all())

    admin_class = site.enabled_admin[app_name][model_name] #get the admin_class class save in the list
    querysets = admin_class.model.objects.all() # get the data

    return render(request, "kingadmin/table_list.html",{"querysets": querysets,"model_name":model_name})
