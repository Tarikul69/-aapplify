from django import forms
from .models import Service, BlogPost, Ticket, Message, ServiceBooking
from django_ckeditor_5.widgets import CKEditor5Widget
from django.forms import TextInput



class TicketForm(forms.ModelForm):
    message = forms.CharField(widget=CKEditor5Widget(attrs={'class': 'django_ckeditor_5'}), required=False)
    class Meta:
        model = Ticket
        fields = ['subject', "message"]

        widgets = {
            'subject': TextInput(attrs={'class': 'p-3 border-b border-black outline-none', 'placeholder': 'Enter your subject'}),
            "message": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}
              )
        }



class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'short_description', 'thumbnail_img', 'description']

class ServiceBookingForm(forms.ModelForm):
    class Meta:
        model = ServiceBooking
        fields = ['title', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].required = False

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}
            ),
        }