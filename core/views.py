from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as authlogout
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.conf import settings
from django.contrib import messages
from .forms import (
    StudentForm,LoginForm,StudentEditForm
    )
User = get_user_model()
signer = TimestampSigner()

def index(request):
    return render(request,"index.html")


def send_verification_email(user):
    token = signer.sign(user.email)
    verification_link = f"http://127.0.0.1:8000/verify-email/{token}/"
    
    subject = "Verify Your Email Address"
    message = f"Click the link below to verify your email:\n\n{verification_link}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    
    send_mail(subject, message, from_email, recipient_list)



def Signup_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password")
            repassword = form.cleaned_data.get("repassword") 
            email=form.cleaned_data.get("email")
           

            if password != repassword:
               form.add_error("repassword", "Passwords do not match.")

            else:
                user_data = form.save(commit=False)
                user_data.set_password(password)
                user_data.is_active = False 
                user_data.username=email,
                user_data.role='student'
                user_data.save()

                send_verification_email(user_data)
                messages.success(request, "Signup successful! Check your email to verify your account.")
                return redirect("login_page") 
    else:
        form = StudentForm()
    return render(request, "signup_student.html", {"form": form})


def verify_email(request, token):
    try:
        email = signer.unsign(token, max_age=86400)  
        user = User.objects.get(email=email)
        user.is_active = True  
        user.save()
        messages.success(request, "Email verified successfully! You can now log in.")
        return redirect("login_page")
    
    except SignatureExpired:
        messages.error(request, "Verification link has expired.")
    except (BadSignature, User.DoesNotExist):
        messages.error(request, "Invalid verification link.")
    
    return redirect("signup_student")



def Login_page(request):
    
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request,user)
                messages.success(request, "Login successful!")
                return redirect("student_dashboard")
            else:
                messages.error(request, "Invalid credentials. Please try again.")
                
    else:
        form=LoginForm()       
    return render(request,"login.html",{'form':form})


def logout(request):
    authlogout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login_page")

def Student_page(request):
    return render(request,"student_dashboard.html")


def Student_Profile(request):
    
    if request.method=="POST":
        form=StudentEditForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("student_profile")
    else:
        form=StudentEditForm(instance=request.user)
    return render(request,"student_profile.html",{'form':form})