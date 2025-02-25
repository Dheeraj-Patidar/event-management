from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout as authlogout
from django.contrib.auth import get_user_model
User = get_user_model()


def index(request):
    return render(request,"index.html")


def Signup_student(request):
    return render(request,"signup_student.html")


def Login_page(request):
    return render(request,"login.html")