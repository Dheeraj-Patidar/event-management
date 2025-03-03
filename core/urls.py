from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    AddEventView,
    AdminView,
    HomeView,
    LoginPageView,
    LogoutView,
    SignupStudentView,
    StudentProfileView,
    StudentView,
    VerifyEmailView,
    EventRegisterView,
    MyEventView,
    EventView,
    ExpiredEventView,
    StudentAccountsView,
    ActivateStudentView,
    MyExpiredEvents
)

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("signup/", SignupStudentView.as_view(), name="signup_student"),
    path("verify-email/<str:token>/", VerifyEmailView.as_view(), name="verify_email"),
    path("login/", LoginPageView.as_view(), name="login_page"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("student_dashboard", StudentView.as_view(), name="student_dashboard"),
    path("student_profile/", StudentProfileView.as_view(), name="student_profile"),
    path("admin_dashboard", AdminView.as_view(), name="admin_dashboard"),
    path("add_events", AddEventView.as_view(), name="add_event"),
    path("event_registration/<int:event_id>", EventRegisterView.as_view(), name="event_register"),
    path("events", EventView.as_view(), name="events"),
    path("expired_events", ExpiredEventView.as_view(), name="expired_events"),
    path("my_events", MyEventView.as_view(), name="my_events"),
    path("student_accounts", StudentAccountsView.as_view(), name="student_accounts"),
    path("activate_student/<int:pk>", ActivateStudentView.as_view(), name="activate_student"),
    path("my_expired_events", MyExpiredEvents.as_view(), name="my_expired_events"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
