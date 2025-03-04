from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
from django.views.generic.edit import FormView

from .forms import AddEventForm, LoginForm, StudentEditForm, StudentForm, RegisterStudentForm
from .models import Event, RegisteredStudent
from .utils import SendVerificationEmailView

User = get_user_model()
signer = TimestampSigner()


class HomeView(TemplateView):
    """home page"""

    template_name = "base.html"


class SignupStudentView(FormView):
    """ "student signup"""

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
    """sending email verification link"""

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
    """Login view for all roles"""

    template_name = "login.html"
    form_class = LoginForm

    def get_success_url(self):
        user = self.request.user
        if user.role == "student":
            return reverse_lazy("student_dashboard")
        elif user.role == "admin":
            return reverse_lazy("admin_dashboard")
        # elif user.role == "staff":
        #     return reverse_lazy("staff_dashboard")
        # return reverse_lazy("login_page")
        return reverse_lazy("login_page")

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
    """logout active user"""

    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect(reverse_lazy("login_page"))


class StudentView(ListView):
    """student dashboard"""

    model = Event
    template_name = "student_dashboard.html"
    context_object_name = "events"

    def get_queryset(self):
        """Return only upcoming events"""
        return Event.objects.filter(date__gte=now()).order_by("date")


class StudentProfileView(LoginRequiredMixin, UpdateView):
    """update student profile"""

    model = User
    form_class = StudentEditForm
    template_name = "student_profile.html"
    success_url = reverse_lazy("student_profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)


class AdminView(TemplateView):
    template_name = "admin_dashboard.html"


class AddEventView(CreateView):
    model = Event
    form_class = AddEventForm
    template_name = "add_event.html"
    success_url = reverse_lazy("add_event")

    def form_valid(self, form):
        messages.success(self.request, "Event added successfully!")
        return super().form_valid(form)


class EventRegisterView(CreateView):
    model = RegisteredStudent
    form_class = RegisterStudentForm
    template_name = "event_registration.html"
    success_url = reverse_lazy("student_dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Registration successfull!")
        return super().form_valid(form)
    
    # def form_valid(self, form):
    #     """Automatically assign student and event"""
    #     event_id = self.kwargs.get("event_id")
    #     event = get_object_or_404(Event, id=event_id)

    #     # Prevent duplicate registration
    #     if RegisteredStudent.objects.filter(student=self.request.user, event=event).exists():
    #         messages.warning(self.request, "You are already registered for this event.")
    #         return self.form_invalid(form)

    #     # Save registration
    #     registration = form.save(commit=False)
    #     registration.student = self.request.user
    #     registration.event = event
    #     registration.save()

    #     messages.success(self.request, "Registration successful!")
    #     return super().form_valid(form)