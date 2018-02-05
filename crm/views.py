from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.
from crm import models,form
from django.views.decorators.csrf import csrf_exempt
import datetime,os,json
from django.conf import settings
from django.utils.timezone import datetime



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
            enrollment_obj.contract_signed_date = datetime.now()
            enrollment_obj.save()

            return HttpResponse("您已成功提交报名信息,请等待审核通过,欢迎加入打死都不退费老男孩教育!")
    else:
        customer_form = form.CustomerInfoForm(instance=enrollment_obj.customer)
    # if request.method == "POST":
    #
    #

    uploaded_files= []
    uploaded_files_dir = os.path.join(settings.UPLOAD_FILES_DIR, str(enrollment_obj.customer_id))

    if os.path.isdir(uploaded_files_dir):

        uploaded_files = os.listdir(uploaded_files_dir)

    return render(request, "crm/enrollment.html",locals())

@csrf_exempt
def enrollment_file_upload(request, enrollment_id):


    enrollment_upload_dir = os.path.join(settings.UPLOAD_FILES_DIR,enrollment_id)

    if not os.path.isdir(enrollment_upload_dir):
        os.mkdir(enrollment_upload_dir)

    file_obj = request.FILES.get('file')

    if len(os.listdir(enrollment_upload_dir)) < 2:
        with open(os.path.join(enrollment_upload_dir,file_obj.name),'wb') as f:
            for chunks in file_obj.chunks():
                f.write(chunks)
    else:
        return HttpResponse(json.dumps({'status':False, 'err_msg':'max upload limit is 2' }))


    return HttpResponse(json.dumps({'status':True,  }))
