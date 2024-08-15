from django import forms
from .models import Category, Thread, Post

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'posted_by', 'category']
        widgets = {
            'posted_by': forms.HiddenInput(),  # hide the field if set automatically by the view
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']
