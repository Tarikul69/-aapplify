from django.urls import path
from .views import RegisterView, LoginView, LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
