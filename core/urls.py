
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index/',views.index,name="index"),
    path("signup_student/",views.Signup_student,name="signup_student"),
    path("verify-email/<str:token>/", views.verify_email, name="verify_email"),
    path('login/',views.Login_page,name="login_page"),
    path('logout/',views.logout,name="logout"),
    path('student_dashboard/',views.Student_page,name="student_dashboard"),
    path('student_profile/',views.Student_Profile,name="student_profile"),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),




]