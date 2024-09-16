from django.shortcuts import render
from django.views.generic import CreateView
from .models import User, RegularUser
from .forms import UserRegisterForm

# Create your views here.
class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'registration/register.html'