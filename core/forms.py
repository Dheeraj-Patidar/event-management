from django import forms
from .models import User
from django.core.validators import RegexValidator

class StudentForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    repassword = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    phone_regex = RegexValidator(
        regex=r'^\d{10}$', message="Phone number must be 10 digits and contain digits only."

    )

    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),validators=[phone_regex])
    
    class Meta:
        model=User
        fields=['first_name','last_name','email','phone_number','password','repassword']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists. Please use a different one.")
        return email


class LoginForm(forms.Form): 
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
   

class StudentEditForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_regex = RegexValidator(
        regex=r'^\d{10}$', message="Phone number must be 10 digits and contain digits only."
    )
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),validators=[phone_regex])
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name',  'phone_number']

    