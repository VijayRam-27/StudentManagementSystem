import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import AddStudentForm, EditStudentForm
from .models import CustomUser, Courses, Staffs, Subjects, Students, SessionYearModel, FeedBackStudent, FeedBackStaff, \
    LeaveReportStudent, LeaveReportStaff, Attendance, AttendanceReport


def admin_home(request):
    students_count = Students.objects.all().count()
    staffs_count = Staffs.objects.all().count()
    course_count = Courses.objects.all().count()
    subject_count = Subjects.objects.all().count()
    courses = Courses.objects.all()
    subjects = Subjects.objects.all()
    course_list = []
    Student_list = []
    for course in courses:
        studenet = Students.objects.filter(course_id=course).count()
        course_list.append(course.course_name)
        Student_list.append(studenet)

    subject_list = []
    for course in courses:
        subject = Subjects.objects.filter(course_id=course).count()
        subject_list.append(subject)

    subject_name_list = []
    subject_student_count = []
    for subject in subjects:
        subject_count = Students.objects.filter(course_id=subject.course_id).count()
        subject_name_list.append(subject.subject_name)
        subject_student_count.append(subject_count)

    return render(request, 'hod_templates/home_content.html',
                  {"students_count": students_count, "staffs_count": staffs_count,
                   "course_count": course_count, "subject_count": subject_count,
                   "course_list": course_list, "Student_list": Student_list,
                   "subject_list": subject_list, "subject_name_list": subject_name_list,
                   "subject_student_count": subject_student_count})


def add_staff(request):
    return render(request, 'hod_templates/add_staff_template.html')


def add_staff_save(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed")
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        user_name = request.POST.get("username")
        address = request.POST.get("address")
        try:
            user = CustomUser.objects.create_user(username=user_name, email=email, password=password,
                                                  first_name=first_name, last_name=last_name, user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, "Staff Added Successfully")
            return HttpResponseRedirect("/add_staff")
        except:
            messages.error(request, "Something Went Wrong.Please Tey Again")
            return HttpResponseRedirect("/add_staff")


def add_course(request):
    return render(request, 'hod_templates/add_course_template.html')


def add_course_save(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed")
    else:
        course_name = request.POST.get("course_name")
        try:
            course_model = Courses(course_name=course_name)
            course_model.save()
            messages.success(request, "Course Added Successfully")
            return HttpResponseRedirect("/add_course")
        except:
            messages.error(request, "Something went wrong")
            return HttpResponseRedirect("/add_course")


def add_student(request):
    courses = Courses.objects.all()
    form = AddStudentForm()
    return render(request, 'hod_templates/add_student.html', {"form": form})


def add_student_save(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed")
    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            user_name = form.cleaned_data["username"]
            address = form.cleaned_data["address"]
            course_id = form.cleaned_data["course"]
            session_year_id = form.cleaned_data["session_year_id"]
            sex = form.cleaned_data["sex"]

            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            file_url = fs.url(filename)

            try:
                user = CustomUser.objects.create_user(username=user_name, email=email, password=password,
                                                      first_name=first_name, last_name=last_name, user_type=3)
                user.students.address = address
                course_obj = Courses.objects.get(id=course_id)
                user.students.course_id = course_obj
                session_year = SessionYearModel.objects.get(id=session_year_id)
                user.students.session_year_id = session_year
                user.students.gender = sex
                user.students.profile_pic = file_url
                user.save()
                messages.success(request, "Student Added Successfully")
                return HttpResponseRedirect("/add_student")
            except:
                messages.error(request, "Something Went Wrong.Please Tey Again")
                return HttpResponseRedirect("/add_student")
        else:
            form = AddStudentForm(request.post)
            return render(request, "hod_templates/add_student.html", {"form": form})


def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, 'hod_templates/add_subject_template.html', {"courses": courses, "staffs": staffs})


def add_subject_save(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed")
    else:
        subject = request.POST.get("subject")
        course_id = request.POST.get("course")
        course = Courses.objects.get(id=course_id)
        staff_id = request.POST.get("staff")
        staff = CustomUser.objects.get(id=staff_id)
        try:
            subject = Subjects(subject_name=subject, course_id=course, staff_id=staff)
            subject.save()
            messages.success(request, "Subject Added Successfully")
            return HttpResponseRedirect("/add_subject")
        except:
            messages.error(request, "Something Went Wrong")
            return HttpResponseRedirect("/add_subject")


def manage_staff(request):
    staffs = Staffs.objects.all()
    return render(request, "hod_templates/manage_staff_template.html", {"staffs": staffs})


def manage_student(request):
    students = Students.objects.all()
    return render(request, "hod_templates/manage_student_template.html", {"students": students})


def manage_course(request):
    courses = Courses.objects.all()
    return render(request, "hod_templates/manage_course_template.html", {"courses": courses})


def manage_subject(request):
    subjects = Subjects.objects.all()
    return render(request, "hod_templates/manage_subject_template.html", {"subjects": subjects})


def edit_staff(request, id):
    staff = Staffs.objects.get(admin=id)
    return render(request, "hod_templates/edit_staff_template.html", {"staff": staff})


def edit_staff_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get("staff_id")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        address = request.POST.get("address")
        try:
            user = CustomUser.objects.get(id=staff_id)
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.save()

            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()

            messages.success(request, "Staff Updated Successfully")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"id": staff_id}))
        except:
            messages.error(request, "Something Went Wrong")
            return HttpResponseRedirect(reverse("edit_staff", kwargs={"id": staff_id}))


def edit_student(request, id):
    request.session["student_id"] = id
    student = Students.objects.get(admin=id)
    courses = Courses.objects.all()
    form = EditStudentForm()
    form.fields["email"].initial = student.admin.email
    form.fields["first_name"].initial = student.admin.first_name
    form.fields["last_name"].initial = student.admin.last_name
    form.fields["username"].initial = student.admin.username
    form.fields["address"].initial = student.address
    form.fields["course"].initial = student.course_id.course_name
    form.fields["sex"].initial = student.gender
    form.fields["session_year_id"].initial = student.session_year_id.id
    form.fields["profile_pic"].initial = student.profile_pic
    return render(request, "hod_templates/edit_student_template.html",
                  {"form": form, "id": id, "username": student.admin.username})


def edit_student_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        std_id = request.session.get("student_id")
        if std_id is not None:
            form = EditStudentForm(request.POST, request.FILES)
            if form.is_valid():
                email = form.cleaned_data["email"]
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                username = form.cleaned_data["username"]
                address = form.cleaned_data["address"]
                course = form.cleaned_data["course"]
                sex = form.cleaned_data["sex"]
                session_year = form.cleaned_data["session_year_id"]
                session_instance = SessionYearModel.objects.get(id=session_year)
                course = Courses.objects.get(id=course)

                if 'profile_pic' in request.FILES:
                    profile_pic = request.FILES['profile_pic']
                    fs = FileSystemStorage()
                    filename = fs.save(profile_pic.name, profile_pic)
                    file_url = fs.url(filename)
                else:
                    file_url = None

                try:
                    user = CustomUser.objects.get(id=std_id)
                    user.email = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.username = username
                    user.save()

                    student_model = Students.objects.get(admin=std_id)
                    student_model.address = address
                    student_model.course_id = course
                    student_model.gender = sex
                    student_model.session_year_id = session_instance
                    if file_url is not None:
                        student_model.profile_pic = file_url
                    student_model.save()
                    del request.session["student_id"]

                    messages.success(request, "Student Successfully Updated")
                    return HttpResponseRedirect("/edit_student/" + std_id)
                except:
                    messages.error(request, "Something Went Wrong")
                    return HttpResponseRedirect("/edit_student/" + std_id)
            else:
                form = EditStudentForm(request.post)
                student = Students.objects.get(admin=std_id)
                return render(request, "hod_templates/edit_student_template.html",
                              {"form": form, "id": id, "username": student.admin.username})

        else:
            return HttpResponseRedirect("/manage_student")


def edit_course(request, id):
    course = Courses.objects.get(id=id)
    return render(request, "hod_templates/edit_course_template.html", {"course": course, "id": id})


def edit_course_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        try:
            course_name = request.POST.get("course_name")
            course_id = request.POST.get("course_id")
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()
            messages.success(request, "Course Successfully Updated")
            return HttpResponseRedirect(reverse("edit_course", args=[course_id]))
        except:
            messages.error(request, "Something Went Wrong.")
            return HttpResponseRedirect(reverse("edit_course", args=[course_id]))


def edit_subject(request, id):
    subject = Subjects.objects.get(id=id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, "hod_templates/edit_subject_template.html",
                  {"subject": subject, "courses": courses, "staffs": staffs, "id": id})


def edit_subject_save(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        try:
            subject_name = request.POST.get("subject")
            sub_id = request.POST.get("subject_id")
            course = request.POST.get("course")
            staff = request.POST.get("staff")

            subject = Subjects.objects.get(id=sub_id)
            subject.subject_name = subject_name
            course_model = Courses.objects.get(id=course)
            staff_model = CustomUser.objects.get(id=staff)
            subject.course_id = course_model
            subject.staff_id = staff_model
            subject.save()

            messages.success(request, "Subject Successfully Updated")
            return HttpResponseRedirect(reverse('edit_subject', args=[sub_id]))
        except:
            messages.error(request, "Something Went Wrong")
            return HttpResponseRedirect(reverse('edit_subject', args=[sub_id]))


def manage_session(request):
    return render(request, "hod_templates/manage_session_template.html")


def add_manage_session(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        try:
            session_start = request.POST.get("session_start")
            session_end = request.POST.get("session_end")
            session_model = SessionYearModel(session_start_year=session_start, session_end_year=session_end)
            session_model.save()

            messages.success(request, "Session Year Added Successfully.")
            return HttpResponseRedirect("/manage_session")
        except:
            messages.error(request, "Something Went Wrong")
            return HttpResponseRedirect("/manage_session")


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user = CustomUser.objects.filter(email=email).exists()
    if user:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user = CustomUser.objects.filter(username=username).exists()
    if user:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    return render(request, "hod_templates/student_feedback_message.html", {"feedbacks": feedbacks})


@csrf_exempt
def student_feedback_message_save(request):
    feedback_id = request.POST.get("feedback_id")
    feedback_reply = request.POST.get("message")

    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("Success")
    except:
        return HttpResponseRedirect(reverse("student_feedback_message"))


def staff_feedback_message(request):
    feedbacks = FeedBackStaff.objects.all()
    return render(request, "hod_templates/staff_feedback_message.html", {"feedbacks": feedbacks})


@csrf_exempt
def staff_feedback_message_save(request):
    feedback_id = request.POST.get("feedback_id")
    feedback_reply = request.POST.get("message")

    try:
        feedback = FeedBackStaff.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("Success")
    except:
        return HttpResponseRedirect(reverse("student_feedback_message"))


def student_leave_view(request):
    student_leave = LeaveReportStudent.objects.all()
    return render(request, "hod_templates/student_leave_view_template.html", {"student_leave": student_leave})


def student_leave_approve(request, leave_id):
    student_leave = LeaveReportStudent.objects.get(id=leave_id)
    student_leave.leave_status = 1
    student_leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def student_leave_disapprove(request, leave_id):
    student_leave = LeaveReportStudent.objects.get(id=leave_id)
    student_leave.leave_status = 2
    student_leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def staff_leave_view(request):
    staff_leave = LeaveReportStaff.objects.all()
    return render(request, "hod_templates/staff_leave_view_template.html", {"staff_leave": staff_leave})


def staff_leave_approve(request, leave_id):
    staff_leave = LeaveReportStaff.objects.get(id=leave_id)
    staff_leave.leave_status = 1
    staff_leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))


def staff_leave_disapprove(request, leave_id):
    staff_leave = LeaveReportStaff.objects.get(id=leave_id)
    staff_leave.leave_status = 2
    staff_leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))


def view_attendance(request):
    subjects = Subjects.objects.all()
    sessions = SessionYearModel.objects.all()
    return render(request, "hod_templates/view_attendance_template.html", {"subjects": subjects, "sessions": sessions})


@csrf_exempt
def get_attendance_dates(request):
    subject = request.POST.get("subject")
    session_id = request.POST.get("session_year")
    attendances = Attendance.objects.filter(subject_id=subject, session_year_id=session_id)
    attendance_obj = []
    for attendance in attendances:
        data = {"id": attendance.id, "attendance_date": str(attendance.attendance_date),
                "subject_id": attendance.subject_id.id, "session_year_id": attendance.session_year_id.id}
        attendance_obj.append(data)
    return JsonResponse(json.dumps(attendance_obj), content_type="application/json", safe=False)


@csrf_exempt
def fetch_student_data(request):
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


def admin_profile_edit(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "hod_templates/admin_edit_profile.html", {"user": user})


def admin_edit_profile_save(request):
    if request.method != "POST":
        HttpResponseRedirect(reverse("admin_home"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(id=request.user.id)
            user.first_name = first_name
            user.last_name = last_name

            if password is not None and password != '':
                user.set_password(password)
            user.save()

            messages.success(request, "Profile Updated Successfuly")
            return HttpResponseRedirect(reverse("admin_profile_edit"))
        except:
            messages.error(request, "Failed To Update")
            return HttpResponseRedirect(reverse("admin_profile_edit"))
