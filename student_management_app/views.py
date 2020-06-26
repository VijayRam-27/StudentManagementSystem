from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.urls import reverse

from .EmailBackEnd import EmailBackEnd


# Create your views here.


def index(request):
    return render(request, 'index.html')


def show_login(request):
    return render(request, 'login.html')


def do_login(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, request.POST.get("email"), request.POST.get("password"))
        if user is not None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect("/admin_home")
            elif user.user_type == "2":
                return HttpResponseRedirect("/staff_home_view")
            elif user.user_type == "3":
                return HttpResponseRedirect("/student_home_view")
        else:
            messages.error(request, "Invalid Credential")
            return HttpResponseRedirect("/show_login")


def do_logout(request):
    logout(request)
    request.user = None
    return HttpResponseRedirect(reverse("show_login"))