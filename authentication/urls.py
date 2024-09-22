from django.urls import path
from .views import RegisterView, LoginView, LogoutView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
        # URL for initiating the password reset
    path('reset_password/',
        auth_views.PasswordResetView.as_view(template_name='pages/password_reset.html'),
        name='password_reset'),

    # URL for after password reset request is done
    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name='pages/password_reset_sent.html'),
        name='password_reset_done'),

    # URL for password reset confirmation link (sent in email)
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='pages/password_reset_form.html'),
        name='password_reset_confirm'),

    # URL for successful password reset
    path('reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='pages/password_reset_done.html'),
        name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
