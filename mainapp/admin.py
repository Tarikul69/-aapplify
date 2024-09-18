from django.contrib import admin
from .models import Service, BlogPost

# Register your models here.

@admin.register(Service)
class UserServiceAdmin(admin.ModelAdmin):
    list = ('id', 'title')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list = ['id', 'title']