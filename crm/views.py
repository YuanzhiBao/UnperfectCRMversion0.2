from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def dashboard(req):
    return render(req, 'crm/dashboard.html')


def stu_enrollment(request):
    return render(request, 'crm/stu_enrollment.html')