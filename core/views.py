from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, UpdateView
from django.views.generic.edit import FormView

from .forms import LoginForm, StudentEditForm, StudentForm
from .utils import SendVerificationEmailView

User = get_user_model()
signer = TimestampSigner()


class HomeView(TemplateView):
    template_name = "base.html"


class SignupStudentView(FormView):
    template_name = "signup_student.html"
    form_class = StudentForm
    success_url = reverse_lazy("login_page")

    def form_valid(self, form):
        password = form.cleaned_data["password"]
        repassword = form.cleaned_data["repassword"]
        email = form.cleaned_data["email"]

        if password != repassword:
            form.add_error("repassword", "Passwords do not match.")
            return self.form_invalid(form)

        user_data = form.save(commit=False)
        user_data.set_password(password)
        user_data.is_active = False
        user_data.username = email
        user_data.role = "student"
        user_data.save()

        SendVerificationEmailView().post(self.request, user_id=user_data.id)
        messages.success(
            self.request, "Signup successful! Check your email to verify your account."
        )

        return super().form_valid(form)


class VerifyEmailView(View):
    def get(self, request, token, *args, **kwargs):
        try:
            email = signer.unsign(token, max_age=86400)
            user = get_object_or_404(User, email=email)
            user.is_active = True
            user.save()
            messages.success(
                request, "Email verified successfully! You can now log in."
            )
            return redirect("login_page")

        except SignatureExpired:
            messages.error(request, "Verification link has expired.")
        except BadSignature:
            messages.error(request, "Invalid verification link.")

        return redirect("signup_student")


class LoginPageView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = reverse_lazy("student_dashboard")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            messages.success(self.request, "Login successful!")
            return super().form_valid(form)

        else:
            messages.error(self.request, "Invalid credentials. Please try again.")
            return self.form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect(reverse_lazy("login_page"))


class StudentView(TemplateView):
    template_name = "student_dashboard.html"


class StudentProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = StudentEditForm
    template_name = "student_profile.html"
    success_url = reverse_lazy("student_profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)
