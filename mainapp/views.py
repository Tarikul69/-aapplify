from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import Service, BlogPost, Ticket, Message, ServiceBooking
from .forms import BlogPostForm, TicketForm
from authentication.models import User

# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'pages/home.html')

class AboutView(View):
    def get(self, request):
        return render(request, 'pages/about.html')

class BlogView(View):
    def get(self, request, blog_id=None):
        if blog_id:
            # Get a single blog post by ID
            blog = get_object_or_404(BlogPost, id=blog_id)
            return render(request, 'pages/blog_detail.html', {'blog': blog})

        # Get all blog posts if no blog_id is provided
        blogs = BlogPost.objects.filter(is_accepted=True)
        return render(request, 'pages/blog.html', {'blogs': blogs})


class ContactView(View):
    def get(self, request):
        return render(request, 'pages/contact.html')

class FAQView(View):
    def get(self, request):
        return render(request, 'pages/faq.html')


class AddBlogView(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    # redirect_field_name = 'redirect_to'


    def get(self, request, slug=None):
        form = BlogPostForm()

        return render(request, 'pages/addblog.html', {'form': form})

    def post(self, request, slug=None):
        form = BlogPostForm(request.POST, request.FILES)
        # form["created_by"] = request.user.pk
        print(request.user)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.created_by = request.user
            blog_post.save()
            form = BlogPostForm()
            messages.success(request, 'Your form has been submitted successfully!')
            return redirect(reverse('add_blog'))
        print(form.is_valid())
        print(form.errors)

        # Form is not valid, render the form with errors
        return render(request, 'pages/addblog.html', {'form': form})

class ServiceView(View):
    def get(self, request, service_id=None):
        if service_id:
            service = get_object_or_404(Service, id=service_id)
            print(service)
            return render(request, 'pages/service_detail.html', {'service': service})

        # List all services
        services = Service.objects.all()
        return render(request, 'pages/services.html', {'services': services})

class TokenView(View):
    def get(self, request):
        form = TicketForm()
        return render(request, 'pages/token.html', context={"form": form})

    def post(self, request, slug=None):
        form = TicketForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            Message.objects.create(
                content=message,
                user=request.user,
                room=ticket
            )
            form = TicketForm()
            return redirect("/")
        print(form.is_valid())
        print(form.errors)

        # Form is not valid, render the form with errors
        return render(request, 'pages/addblog.html', {'form': form})



class BlogPostView(View):
    def get(self, request, slug=None):
        if slug:
            # Edit an existing blog post
            blog_post = get_object_or_404(BlogPost, slug=slug)
            form = BlogPostForm(instance=blog_post)
        else:
            # Create a new blog post
            form = BlogPostForm()

        return render(request, 'pages/blog_post_form.html', {'form': form})

    def post(self, request, slug=None):
        if slug:
            # Update an existing blog post
            blog_post = get_object_or_404(BlogPost, slug=slug)
            form = BlogPostForm(request.POST, request.FILES, instance=blog_post)
        else:
            # Create a new blog post
            form = BlogPostForm(request.POST, request.FILES)

        if form.is_valid():
            blog_post = form.save()
            return redirect(reverse('blog_post_detail', args=[blog_post.slug]))

        return render(request, 'pages/blog_post_form.html', {'form': form})

class ProfileView(View):

    def get(self, request):
        profile = get_object_or_404(User, email=request.user)
        blogs = BlogPost.objects.filter(created_by=profile)
        booking = ServiceBooking.objects.filter(user=profile)

        context = {
        'profile': profile,
        'blogs': blogs,
        'booking': booking,
            }

        return render(request, 'pages/profile.html', context)

# class ServiceListView(ListView):
#     model = Service
#     template_name = 'service_list.html'
#     context_object_name = 'services'

# class ServiceDetailView(DetailView):
#     model = Service
#     template_name = 'service_detail.html'
#     context_object_name = 'service'

# class ServiceCreateView(CreateView):
#     model = Service
#     form_class = ServiceForm
#     template_name = 'service_form.html'
#     success_url = reverse_lazy('service-list')

# class ServiceUpdateView(UpdateView):
#     model = Service
#     form_class = ServiceForm
#     template_name = 'service_form.html'
#     success_url = reverse_lazy('service-list')

# class ServiceDeleteView(DeleteView):
#     model = Service
#     template_name = 'service_confirm_delete.html'
#     success_url = reverse_lazy('service-list')