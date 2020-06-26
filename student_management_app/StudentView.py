from django.shortcuts import render


def student_home_view(request):
    return render(request, "student_templates/student_home_template.html")