# from django.shortcuts import render
# from django.views.generic import CreateView
# from .models import User, RegularUser
# from .forms import UserRegisterForm

# # Create your views here.
# class UserRegisterView(CreateView):
#     model = User
#     form_class = UserRegisterForm
#     template_name = 'registration/register.html'

from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'pages/register.html', {'registration_form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            if account is not None:
                login(request, account)
                return redirect('main_home')
        return render(request, 'pages/register.html', {'registration_form': form})

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("main_home")

        form = UserLoginForm()
        return render(request, "pages/login.html", {'login_form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("main_home")

        # If form is not valid, or authentication fails, re-render the form with errors
        return render(request, "pages/login.html", {'login_form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main_home')