from django import forms
from .models import Service, BlogPost
from django_ckeditor_5.widgets import CKEditor5Widget


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'short_description', 'thumbnail_img', 'description']


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'thumbnail', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'bg-slate-300 w-full p-4 text-lg rounded-lg mt-3'}),
            # 'slug': forms.TextInput(attrs={'class': 'bg-slate-300 w-full p-4 text-lg rounded-lg mt-3'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'bg-slate-300 w-full p-4 text-lg rounded-lg mt-3'}),
            "body": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}
              )
        }