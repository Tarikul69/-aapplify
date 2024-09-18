from django.urls import path
from .views import HomeView, AboutView, BlogView, ContactView, FAQView, ServiceView, AddBlogView, BlogPostView, TokenView

urlpatterns = [
    path('', HomeView.as_view(), name='main_home'),
    path('about/', AboutView.as_view(), name='main_about'),
    path('blog/', BlogView.as_view(), name='main_blog'),
    path('contact/', ContactView.as_view(), name='main_contact'),
    path('faq/',FAQView.as_view(), name='main_faq'),
    path('service/', ServiceView.as_view(), name='main_services'),
    path('services/<int:service_id>/', ServiceView.as_view(), name='service-detail'),
    path('addblog/', AddBlogView.as_view(), name='add_blog'),
    path('blog/<slug:slug>/', AddBlogView.as_view(), name='edit_blog'),  # Use the same view for editing
    path('token/', TokenView.as_view(), name='main_token')
    # path('blog/<slug:slug>/detail/', BlogPostDetailView.as_view(), name='blog_post_detail'),
]
