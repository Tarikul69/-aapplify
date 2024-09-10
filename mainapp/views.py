from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect

# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'pages/home.html')

class AboutView(View):
    def get(self, request):
        return render(request, 'pages/about.html')

class BlogView(View):
    def get(self, request):
        return render(request, 'pages/blog.html')

class ContactView(View):
    def get(self, request):
        return render(request, 'pages/contact.html')

class FAQView(View):
    def get(self, request):
        return render(request, 'pages/faq.html')

class ServiceView(View):
    def get(self, request):
        return render(request, 'pages/services.html')