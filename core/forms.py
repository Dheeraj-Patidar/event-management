from django import forms
from django.core.validators import RegexValidator
from django.utils.timezone import now
from .models import Event, User, RegisteredStudent  


class StudentForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    repassword = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    password_regex = RegexValidator(
        regex=r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
        message="Password must have at least 8 characters, one uppercase, one lowercase, one number, and one special character.",
    )
    phone_regex = RegexValidator(
        regex=r"^\d{10}$",
        message="Phone number must be 10 digits and contain digits only.",
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        validators=[password_regex],
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[phone_regex],
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password",
            "repassword",
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email already exists. Please use a different one."
            )
        return email


class LoginForm(forms.Form):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class StudentEditForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    phone_regex = RegexValidator(
        regex=r"^\d{10}$",
        message="Phone number must be 10 digits and contain digits only.",
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[phone_regex],
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number"]


class AddEventForm(forms.ModelForm):
    event_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        
    )
    description = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        ), required=True
    )
    location = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
     
    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date and date < now():
            raise forms.ValidationError("The event date must be in the future!")
        return date
    
    class Meta:
        model = Event
        fields = ["event_name", "description", "date", "location"]
    
    

class RegisterStudentForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email_regex = RegexValidator(
        regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        message="Enter a valid email address.",
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"}),
        validators=[email_regex],
    )
    phone_regex = RegexValidator(
        regex=r"^\d{10}$",
        message="Phone number must be 10 digits and contain digits only."
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        validators=[phone_regex],
    )

    class Meta:
        model = RegisteredStudent  
        fields = ["first_name", "last_name", "email", "phone_number"]