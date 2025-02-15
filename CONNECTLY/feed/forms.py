from django import forms
from .models import Post, Profile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']
        labels = {
            'image': 'Upload Image',
            'caption': 'Write a Caption',
        }
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write something about your post...'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']
        labels = {
            'profile_picture': 'Profile Picture',
            'bio': 'Short Bio',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself...'}),
        }

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        if len(bio) > 500:
            raise forms.ValidationError("Bio cannot exceed 500 characters.")
        return bio
