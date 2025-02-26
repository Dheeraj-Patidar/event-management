from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout as authlogout
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import UserForm
User = get_user_model()


def index(request):
    return render(request,"index.html")


def Signup_student(request):
    if request.method == "POST":
        form = UserForm(request.POST)
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
        form = UserForm()

    return render(request, "signup_student.html", {"form": form})




def Login_page(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(email,password)
        if not user:
            return render(request, "login.html")
        user = authenticate(request, username=email, password=password)
        print(user)
        if user is not None:
            login(request,user)
            return redirect("student_dashboard")
        # else:
        #     return render(request, "login.html")
    
    return render(request,"login.html")



def Student_page(request):
    return render(request,"student_dashboard")