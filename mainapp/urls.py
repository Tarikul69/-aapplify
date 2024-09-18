from django.urls import path
from .views import HomeView, AboutView, BlogView, ContactView, FAQView, ServiceView

urlpatterns = [
    path('', HomeView.as_view(), name='main_home'),
    path('about/', AboutView.as_view(), name='main_about'),
    path('blog/', BlogView.as_view(), name='main_blog'),
    path('contact/', ContactView.as_view(), name='main_contact'),
    path('faq/',FAQView.as_view(), name='main_faq'),
    path('service/', ServiceView.as_view(), name='main_services'),
    path('services/<int:service_id>/', ServiceView.as_view(), name='service-detail'),
]
