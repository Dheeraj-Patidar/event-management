
from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index,name="index"),
    path("signup_student/",views.Signup_student,name="signup_student"),
    path('login/',views.Login_page,name="login_page"),
    path('logout/',views.logout,name="logout"),
    path('student_dashboard',views.Student_page,name="student_dashboard"),

]