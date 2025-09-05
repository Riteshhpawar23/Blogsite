from django import forms
from .models import create_blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = create_blog
        fields = ['title', 'slug', 'Author_name', 'content', 'image', 'Category']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter blog title'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'blog-url-slug'
            }),
            'Author_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Your name'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent h-32',
                'placeholder': 'Write your blog content here...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'Category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
        }
        
        labels = {
            'title': 'Blog Title',
            'slug': 'URL Slug',
            'Author_name': 'Author Name',
            'content': 'Blog Content',
            'image': 'Blog Image',
            'Category': 'Category',
        }
