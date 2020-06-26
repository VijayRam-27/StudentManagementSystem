import json

from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Subjects, SessionYearModel, Courses, Students, Attendance, AttendanceReport


def staff_home_view(request):
    return render(request, "staff_templates/staff_home_template.html")


def staff_take_attendance(request):
    staff_id = request.user.id
    subjects = Subjects.objects.filter(staff_id=staff_id)
    sessions = SessionYearModel.objects.all()
    return render(request, "staff_templates/staff_take_attendance.html", {"subjects": subjects, "sessions": sessions})


@csrf_exempt
def get_student(request):
    subject = request.POST.get("subject")
    session = request.POST.get("session_year")
    subject = Subjects.objects.get(id=subject)
    session = SessionYearModel.objects.get(id=session)
    students = Students.objects.filter(course_id=subject.course_id, session_year_id=session)
    student_list = serializers.serialize("python", students)
    list_data=[]
    for student in students:
        data_set = {"id":student.admin.id, "name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_set)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)



@csrf_exempt
def save_student_attendance(request):
    student_ids = request.POST.get("student_ids")
    attendance_date = request.POST.get("attendance_date")
    subject_id = request.POST.get("subject_id")
    session_year_id = request.POST.get("session_year_id")

    try:
        subject = Subjects.objects.get(id=subject_id)
        SessionYearModel.objects.get(id=session_year_id)
        attendance = Attendance(subject_id=subject, attendance_date=attendance_date)
        attendance.save()

        dict_datas = json.loads(student_ids)
        for dict in dict_datas:
            student = Students.objects.get(admin=dict["id"])
            attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=dict["status"])
            attendance_report.save()

        return HttpResponse("success")
    except:
        return HttpResponseRedirect("error")






