from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

import stripe

from .models import Service, BlogPost, Ticket, Message, ServiceBooking, Payment
from .forms import BlogPostForm, TicketForm, MessageForm
from authentication.models import User

stripe.api_key = 'your_stripe_secret_key'

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

class TokenView(View):
    def get(self, request):
        # Fetch the tickets for the logged-in user
        if request.user.is_staff:
            tickets = Ticket.objects.all()
        else:
            tickets = Ticket.objects.filter(user=request.user)
        form = TicketForm()
        return render(request, 'pages/token.html', context={"form": form, "tickets": tickets})


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
            return redirect(reverse('main_token'))
        print(form.is_valid())
        print(form.errors)

        # Form is not valid, render the form with errors
        return render(request, 'pages/addblog.html', {'form': form})

class TicketDetailView(View):
    def get(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        messages = Message.objects.filter(room=ticket)
        form = MessageForm()  # Initialize the form
        return render(request, 'pages/ticket_detail.html', {'ticket': ticket, 'messages': messages, 'form': form})

    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk, user=request.user)
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.room = ticket  # Associate message with the ticket
            message.user = request.user  # Assuming the user is logged in
            message.save()
            return redirect('ticket_detail', pk=ticket.id)  # Redirect to the ticket detail page

        messages = Message.objects.filter(room=ticket)
        return render(request, 'pages/ticket_detail.html', {'ticket': ticket, 'messages': messages, 'form': form})



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

class ServiceView(View):
    def get(self, request, service_id=None):
        if service_id:
            service = get_object_or_404(Service, id=service_id)
            print(service)
            return render(request, 'pages/service_detail.html', {'service': service})

        # List all services
        services = Service.objects.all()
        return render(request, 'pages/services.html', {'services': services})

@login_required(login_url="/auth/login/")
def create_checkout_session(request):
    if request.method == "POST":
        print("enter post method")
        price_id = request.POST.get("price_id")
        service_id = request.POST.get("service_id")
        user = request.user  # Get the logged-in user
        print(user)

        # Create a new booking with pending status
        booking = ServiceBooking.objects.create(
            service=get_object_or_404(Service, id=service_id),
            user=user,
            title=request.POST.get("title"),
            price=request.POST.get("price")  # Ensure you're getting the price from the form
        )

        try:
            # Create the Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=request.build_absolute_uri(reverse("success", kwargs={'booking_id': booking.id})),
                cancel_url=request.build_absolute_uri(reverse("cancel")),
            )
            return redirect(checkout_session.url, code=303)
        except Exception as e:
            print(e)
            booking.delete()
            raise Exception("error")

    return redirect('main_services')

def success(request, booking_id):
    booking = get_object_or_404(ServiceBooking, id=booking_id)

    # Retrieve the Stripe session ID
    session_id = request.GET.get('session_id')
    if session_id:
        try:
            # Retrieve the session to confirm payment
            checkout_session = stripe.checkout.Session.retrieve(session_id)
            if checkout_session.payment_status == 'paid':
                # Save payment information
                Payment.objects.create(
                    booking=booking,
                    user=booking.user,
                    stripe_payment_intent_id=checkout_session.payment_intent,
                    amount=booking.price,
                    status='succeeded',
                )
                # Update the booking status to confirmed
                booking.status = 'confirmed'
                booking.save()
        except Exception as e:
            return str(e)

    return render(request, "pages/success.html")

def cancel(request):
    return render(request, "pages/cancel.html")