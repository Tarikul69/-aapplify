from django.contrib import admin
from .models import Service

# Register your models here.

@admin.register(Service)
class UserService(admin.ModelAdmin):
    list = ('id', 'title')