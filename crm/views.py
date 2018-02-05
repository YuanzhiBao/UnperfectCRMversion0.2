from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from crm import models,form
import datetime


@login_required
def dashboard(req):
    return render(req, 'crm/dashboard.html')



@login_required
def stu_enrollment(request):

    customers = models.CustomerInfo.objects.all()
    class_lists = models.ClassList.objects.all()

    if request.method == "POST":
        customer_id = request.POST.get("customer_id")
        class_grade_id = request.POST.get("class_id")
        enrollment_obj = models.StudentEnrollment.objects.create(
            customer_id = customer_id,
            class_grade_id= class_grade_id,
            consultant_id = request.user.userprofile.id,
        )

        enrollment_link = "http://localhost:8000/crm/enrollment/%s/" % enrollment_obj.id

    return render(request,'crm/stu_enrollment.html',locals())



def enrollment(request, enrollment_id):
    '''学员在线报名表地址'''

    enrollment_obj = models.StudentEnrollment.objects.get(id=enrollment_id)

    customer_info = models.CustomerInfo.objects.get(id=enrollment_obj.customer_id)

    customer_form = form.CustomerInfoForm(instance=customer_info)

    if request.method == "POST":
        customer_form = form.CustomerInfoForm(instance=customer_info, data=request.POST)
        if customer_form.is_valid():
            print("customer_form_obj from view-->>>",customer_form)
            customer_form.save()
            enrollment_obj.contract_agreed = True
            enrollment_obj.contract_signed_date = datetime.datetime.now()
            enrollment_obj.save()

            return HttpResponse("您已成功提交报名信息,请等待审核通过,欢迎加入打死都不退费老男孩教育!")
    else:
        customer_form = form.CustomerInfoForm(instance=enrollment_obj.customer)
    # if request.method == "POST":
    #
    #


    return render(request, "crm/enrollment.html",locals())