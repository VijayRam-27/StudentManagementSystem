from django import forms
from .models import Courses, SessionYearModel


class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label='First Name', max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label='Last Name', max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label='User Name', max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label='Address', max_length=100, widget=forms.TextInput(attrs={"class":"form-control"}))
    course_choice = []
    try:
        courses = Courses.objects.all()
        for course in courses:
            course_list = (course.id, course.course_name)
            course_choice.append(course_list)
    except:
        course_choice = []
    course = forms.ChoiceField(label='Course', choices=course_choice, widget=forms.Select(attrs={"class":"form-control"}))
    gender_choice = (("male", "Male"), ("female", "Female"))
    sex = forms.ChoiceField(label='Sex', choices=gender_choice, widget=forms.Select(attrs={"class":"form-control"}))
    sessions = SessionYearModel.objects.all()
    session_list = []
    for session in sessions:
        session_arr = (session.id, "From "+str(session.session_start_year) + " - To " + str(session.session_end_year))
        session_list.append(session_arr)
    session_year_id = forms.ChoiceField(label='Session Year',choices=session_list, widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic = forms.FileField(label='Profile Pic', widget=forms.FileInput(attrs={"class":"form-control"}))


class DateInput(forms.DateInput):
    input_type = "date"


class EditStudentForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50, widget=forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}))
    first_name = forms.CharField(label='First Name', max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label='Last Name', max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label='User Name', max_length=50, widget=forms.TextInput(attrs={"class":"form-control", "autocomplete":"off"}))
    address = forms.CharField(label='Address', max_length=100, widget=forms.TextInput(attrs={"class":"form-control"}))
    course_choice=[]
    try:
        courses = Courses.objects.all()
        for course in courses:
            course_list = (course.id, course.course_name)
            course_choice.append(course_list)
    except:
        course_choice =[]
    sessions = SessionYearModel.objects.all()
    session_list = []
    for session in sessions:
        session_arr = (session.id, "From "+str(session.session_start_year) + " - To " + str(session.session_end_year))
        session_list.append(session_arr)
    course = forms.ChoiceField(label='Course', choices=course_choice, widget=forms.Select(attrs={"class":"form-control"}))
    gender_choice = (("male", "Male"), ("female", "Female"))
    sex = forms.ChoiceField(label='Sex', choices=gender_choice, widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id = forms.ChoiceField(label='Session Year', choices=session_list, widget=forms.Select(attrs={"class": "form-control"}))
    profile_pic = forms.FileField(label='Profile Pic', widget=forms.FileInput(attrs={"class":"form-control"}), required=False)
