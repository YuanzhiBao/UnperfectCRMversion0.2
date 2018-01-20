from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout
from kingadmin.sites import site
from kingadmin.app_setup import discover

discover()

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
        print(request.GET.get('next'))
        print(request.GET.get)
        if user:
            login(request,user)
            return redirect(request.GET.get('next','/'))
        else:
            return render(request, "signin.html",{"error_msg": "wrongwrong!"})
    else:
        return render(request, "signin.html")


def signout(request):
    logout(request)
    return redirect('/signin/')