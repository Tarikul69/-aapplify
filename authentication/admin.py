from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class UserModelAdmin(UserAdmin):
    list_display = ('pk', 'username', 'email', "phone", "is_superuser", "is_staff",)
    search_fields = ("username", "email", "phone")

admin.site.register(User)
