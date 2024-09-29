from django.contrib import admin
from .models import Service, BlogPost, Ticket, Message, ServiceBooking

# Register your models here.

@admin.register(Service)
class UserServiceAdmin(admin.ModelAdmin):
    list = ('id', 'title')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list = ['id', 'title']


admin.site.register(Ticket)
admin.site.register(Message)
admin.site.register(ServiceBooking)
