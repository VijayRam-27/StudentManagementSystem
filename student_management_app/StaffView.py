import json

from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Subjects, SessionYearModel, Courses, Students, Attendance, AttendanceReport, Staffs, \
    LeaveReportStaff, FeedBackStaff, CustomUser


def staff_home_view(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    course_list = []
    subject_name_list = []
    subject_attend_list = []
    for subject in subjects:
        sub_attend = Attendance.objects.filter(subject_id=subject.id).count()
        subject_attend_list.append(sub_attend)
        sub_name = subject.subject_name
        subject_name_list.append(sub_name)
        course = Courses.objects.get(id=subject.course_id.id)
        course_list.append(course.id)

    final_list = []
    for course_count in course_list:
        if course_count not in final_list:
            final_list.append(course_count)

    student_count = Students.objects.filter(course_id__in=final_list).count()
    attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()
    staff = Staffs.objects.get(admin=request.user.id)
    leave_count = LeaveReportStaff.objects.filter(staff_id=staff, leave_status=1).count()
    subject_count = subjects.count()

    student_list = Students.objects.filter(course_id__in=final_list)
    student_name_list = []
    student_present_list = []
    student_absent_list = []
    for student in student_list:
        student_present = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
        student_absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
        student_name_list.append(student.admin.username)
        student_present_list.append(student_present)
        student_absent_list.append(student_absent)

    return render(request, "staff_templates/staff_home_template.html",
                  {"student_count": student_count, "attendance_count": attendance_count,
                   "leave_count": leave_count, "subject_count": subject_count,
                   "subject_attend_list": subject_attend_list, "subject_name_list": subject_name_list,
                   "student_name_list":student_name_list, "student_present_list":student_present_list, "student_absent_list":student_absent_list})


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
    list_data = []
    for student in students:
        data_set = {"id": student.admin.id, "name": student.admin.first_name + " " + student.admin.last_name}
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
        session = SessionYearModel.objects.get(id=session_year_id)
        attendance = Attendance(subject_id=subject, attendance_date=attendance_date, session_year_id=session)
        attendance.save()

        dict_datas = json.loads(student_ids)
        for dict in dict_datas:
            student = Students.objects.get(admin=dict["id"])
            attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=dict["status"])
            attendance_report.save()

        return HttpResponse("success")
    except:
        return HttpResponseRedirect("error")


def staff_update_attendance_view(request):
    staff_id = request.user.id
    subjects = Subjects.objects.filter(staff_id=staff_id)
    sessions = SessionYearModel.objects.all()
    return render(request, "staff_templates/staff_update_attendance_view.html",
                  {"subjects": subjects, "sessions": sessions})


@csrf_exempt
def get_attendance_dates(request):
    subject_id = request.POST.get("subject")
    session_year_id = request.POST.get("session_year")
    subject = Subjects.objects.get(id=subject_id)
    session_model = SessionYearModel.objects.get(id=session_year_id)
    attendances = Attendance.objects.filter(subject_id=subject, session_year_id=session_model)
    attendance_obj = []
    for attendance in attendances:
        data = {"id": attendance.id, "attendance_date": str(attendance.attendance_date),
                "subject_id": attendance.subject_id.id, "session_year_id": attendance.session_year_id.id}
        attendance_obj.append(data)
    return JsonResponse(json.dumps(attendance_obj), content_type="application/json", safe=False)


@csrf_exempt
def fetch_student_data(request):
    subject = request.POST.get("subject")
    session = request.POST.get("session_year")
    attendance_date_id = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date_id)
    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []
    for student in attendance_data:
        data_set = {"id": student.student_id.id,
                    "name": student.student_id.admin.first_name + " " + student.student_id.admin.last_name,
                    "status": student.status}
        list_data.append(data_set)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def save_update_attendance_data(request):
    student_ids = request.POST.get("student_ids")
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)
    json_students = json.loads((student_ids))
    try:
        for dict in json_students:
            student = Students.objects.get(id=dict["id"])
            attendance_report = AttendanceReport.objects.get(student_id=student, attendance_id=attendance)
            attendance_report.status = dict["status"]
            attendance_report.save()
        return HttpResponse("success")
    except:
        return HttpResponseRedirect("error")


def staff_apply_leave(request):
    staff = Staffs.objects.get(admin=request.user.id)
    leave_reports = LeaveReportStaff.objects.filter(staff_id=staff)
    return render(request, "staff_templates/staff_apply_leave_template.html", {"leave_reports": leave_reports})


def staff_feedback(request):
    staff = Staffs.objects.get(admin=request.user.id)
    feedback = FeedBackStaff.objects.filter(staff_id=staff)
    return render(request, "staff_templates/staff_feedback_template.html", {"feedback": feedback})


def staff_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_message")
        staff = Staffs.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStaff(staff_id=staff, leave_date=leave_date, leave_message=leave_msg,
                                            leave_status=0)
            leave_report.save()

            messages.success(request, "Leave Applied Successfully")
            return HttpResponseRedirect("staff_apply_leave")
        except:
            messages.error(request, "Failed To Apply Leave")
            return HttpResponseRedirect("staff_apply_leave")


def staff_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_feedback"))
    else:
        staff = Staffs.objects.get(admin=request.user.id)
        feedback = request.POST.get("feedback")
        try:
            feedback_model = FeedBackStaff(staff_id=staff, feedback=feedback)
            feedback_model.save()

            messages.success(request, "Feedback Saved Successfully")
            return HttpResponseRedirect("staff_feedback")
        except:
            messages.error(request, "Failed To Save Feedback")
            return HttpResponseRedirect("staff_feedback")


def staff_edit_profile(request):
    staff = Staffs.objects.get(admin=request.user.id)
    return render(request, "staff_templates/staff_edit_profile_template.html", {"staff": staff})


def staff_edit_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_home_view"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(id=request.user.id)
            user.first_name = first_name
            user.last_name = last_name
            if password is not None and password != '':
                user.set_password(password)
            user.save()

            staff = Staffs.objects.get(admin=request.user.id)
            staff.address = address
            staff.save()

            messages.success(request, "Profile Updated Successfully")
            return HttpResponseRedirect(reverse("staff_edit_profile"))
        except:
            messages.error(request, "Failed To update")
            return HttpResponseRedirect(reverse("staff_edit_profile"))
