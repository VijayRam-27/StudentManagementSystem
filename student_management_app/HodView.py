from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import AddStudentForm, EditStudentForm
from .models import CustomUser, Courses, Staffs, Subjects, Students, SessionYearModel


def admin_home(request):
    return render(request, 'hod_templates/home_content.html')


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

            #try:
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
            # except:
            #     messages.error(request, "Something Went Wrong.Please Tey Again")
            #     return HttpResponseRedirect("/add_student")
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