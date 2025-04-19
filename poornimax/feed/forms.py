# feed/forms.py
from django import forms
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a caption...'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 2, 
                'placeholder': 'Write your comment here...',
                'class': 'comment-popup-input'
            }),
        }

class ConfessionForm(forms.ModelForm):
    class Meta:
        model = Confession
        fields = ['content', 'is_anonymous']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your confession here...'}),
        }