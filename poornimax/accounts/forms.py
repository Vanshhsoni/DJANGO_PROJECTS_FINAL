from django import forms
from django.core.exceptions import ValidationError
from .models import User  # Assuming a custom User model

class SignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

    class Meta:
        model = User
        fields = ['full_name', 'college_email', 'username', 'password', 'confirm_password', 'dob',
                  'college', 'department', 'gender', 'bio', 'profile_picture']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already taken.")
        return username

    def clean_college_email(self):
        email = self.cleaned_data['college_email']
        if not email.endswith('@poornima.org'):
            raise ValidationError("Use your @poornima.org college email.")
        if User.objects.filter(college_email=email).exists():
            raise ValidationError("Email already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")
        if password and confirm and password != confirm:
            raise ValidationError("Passwords do not match.")
