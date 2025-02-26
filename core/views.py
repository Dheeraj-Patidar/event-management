from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout as authlogout
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import StudentForm,LoginForm
User = get_user_model()


def index(request):
    return render(request,"index.html")


def Signup_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            phone_number = form.cleaned_data.get("phone_number")
            password = form.cleaned_data.get("password")
            repassword = form.cleaned_data.get("repassword") 
            
            if password != repassword:
               form.add_error("repassword", "Passwords do not match.")

            else:
                user_data = User.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    username=email,
                    role='student'
                )
                user_data.set_password(password) 
                user_data.save()

                messages.success(request, "Signup successful! You can now log in.")
                return redirect('login_page')  
            

    else:
        form = StudentForm()

    return render(request, "signup_student.html", {"form": form})




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