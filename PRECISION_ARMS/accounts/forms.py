from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'address', 'phone_number']  # Make sure 'profile_picture' is included
        widgets = {
            'profile_picture': forms.FileInput(attrs={'accept': 'image/*'}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter new address'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter phone number', 'pattern': '[0-9]*', 'inputmode': 'numeric'}),
        }
