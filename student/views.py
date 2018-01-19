from django.shortcuts import render, HttpResponse

# Create your views here.


def student_index(req):
    return HttpResponse("from student")
