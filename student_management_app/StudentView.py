import datetime
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Students, Courses, Subjects, Attendance, AttendanceReport, LeaveReportStudent, FeedBackStudent, \
    CustomUser


def student_home_view(request):
    student_obj = Students.objects.get(admin=request.user.id)
    subjects_count = Subjects.objects.filter(course_id=student_obj.course_id).count()
    all_attendance = AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_present = AttendanceReport.objects.filter(student_id=student_obj, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(student_id=student_obj, status=False).count()

    subjects = Subjects.objects.filter(course_id=student_obj.course_id)
    all_present = []
    all_absent = []
    subjects_all = []
    for sub in subjects:
        subject_name = sub.subject_name
        attendance = Attendance.objects.filter(subject_id=sub.id)
        present_data = AttendanceReport.objects.filter(student_id = student_obj, attendance_id__in=attendance, status=True).count()
        absent_data = AttendanceReport.objects.filter(student_id = student_obj, attendance_id__in=attendance, status=False).count()
        all_present.append(present_data)
        all_absent.append(absent_data)
        subjects_all.append(subject_name)
    return render(request, "student_templates/student_home_template.html",
                  {"all_attendance": all_attendance, "attendance_present": attendance_present,
                   "attendance_absent": attendance_absent, "subjects_count": subjects_count, "subjects": subjects_all,
                   "present": all_present, "absent": all_absent})


def student_view_attendance(request):
    student = Students.objects.get(admin=request.user.id)
    course = Courses.objects.get(id=student.course_id.id)
    subjects = Subjects.objects.filter(course_id=course)
    return render(request, "student_templates/student_view_attendance_template.html", {"subjects": subjects})


def student_view_attendance_post(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse("student_view_attendance"))
    else:
        subject = request.POST.get("subject")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        start_date_format = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_format = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        subject = Subjects.objects.get(id=subject)
        student = Students.objects.get(admin=request.user.id)
        attendance = Attendance.objects.filter(attendance_date__range=(start_date_format, end_date_format),
                                               subject_id=subject)
        attendance_report = AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=student)

        return render(request, "student_templates/student_view_attendance_data.html",
                      {"attendances": attendance_report})


def student_apply_leave(request):
    student = Students.objects.get(admin=request.user.id)
    leave_reports = LeaveReportStudent.objects.filter(student_id=student)
    return render(request, "student_templates/student_apply_leave_template.html", {"leave_reports": leave_reports})


def student_feedback(request):
    student = Students.objects.get(admin=request.user.id)
    feedback = FeedBackStudent.objects.filter(student_id=student)
    return render(request, "student_templates/student_feedback_template.html", {"feedback": feedback})


def student_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_message")
        student = Students.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudent(student_id=student, leave_date=leave_date, leave_message=leave_msg,
                                              leave_status=0)
            leave_report.save()

            messages.success(request, "Leave Applied Successfully")
            return HttpResponseRedirect("student_apply_leave")
        except:
            messages.error(request, "Failed To Apply Leave")
            return HttpResponseRedirect("student_apply_leave")


def student_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("staff_feedback"))
    else:
        student = Students.objects.get(admin=request.user.id)
        feedback = request.POST.get("feedback")
        try:
            feedback_model = FeedBackStudent(student_id=student, feedback=feedback)
            feedback_model.save()

            messages.success(request, "Feedback Saved Successfully")
            return HttpResponseRedirect("student_feedback")
        except:
            messages.error(request, "Failed To Save Feedback")
            return HttpResponseRedirect("student_feedback")


def student_profile_edit(request):
    student = Students.objects.get(admin=request.user.id)
    return render(request, "student_templates/student_edit_profile.html", {"student": student})


def student_edit_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_home_view"))
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
            student = Students.objects.get(admin=request.user.id)
            student.address = address
            student.save()

            messages.success(request, "Profile Updated Successfully")
            return HttpResponseRedirect(reverse("student_profile_edit"))
        except:
            messages.error(request, "Failed To Update")
            return HttpResponseRedirect(reverse("student_profile_edit"))
