from django.shortcuts import render
from django.views import View, generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse

import stripe
from django.conf import settings

from .models import (BlogPost, CreditTransaction, Fulfillment, Message, Service, ServiceBooking,
    Ticket)
from .forms import BlogPostForm, TicketForm, MessageForm
from authentication.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

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


class CreateCheckoutSessionView(generic.View):
    def post(self, *args, **kwargs):
        try:
            host = self.request.get_host()
            # Get service price dynamically from POST data
            service_id = self.request.POST['service_id']

            # Fetch service details from the database
            service = get_object_or_404(Service, id=int(service_id))

            # Convert price to an integer (in the smallest currency unit, such as poisha for BDT)
            price_in_cents = int(float(service.price) * 100)

            # Create a Checkout Session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': price_in_cents,  # Unit amount in the smallest currency unit
                            'product_data': {
                                'name': service.title,  # Name of the product
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=f"http://{host}{reverse('success')}",
                cancel_url=f"http://{host}{reverse('cancel')}",
                metadata={
                    'service_id': str(service.id),
                    'user_id': str(self.request.user.id)  # Assuming the user is logged in
                }
            )

            return redirect(checkout_session.url, code=303)
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)


def success(request, booking_id):
    return render(request, "pages/success.html")

def cancel(request):
    return render(request, "pages/cancel.html")


def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed' or event['type'] == 'checkout.session.async_payment_succeeded':
        session = event['data']['object']
        fulfill_checkout(session)

    return HttpResponse(status=200)

def fulfill_checkout(session):
    session_id = session['id']

    # Check if the fulfillment has already been done for this session
    if Fulfillment.objects.filter(session_id=session_id, fulfilled=True).exists():
        print(f"Session {session_id} has already been fulfilled.")
        return

    # Retrieve the line items and metadata from the session
    checkout_session = stripe.checkout.Session.retrieve(
        session_id,
        expand=['line_items'],
    )

    # Extract service details from metadata
    service_id = checkout_session.metadata['service_id']
    user_id = checkout_session.metadata['user_id']

    # Fetch the service and user from the database
    service = get_object_or_404(Service, id=int(service_id))
    user = get_object_or_404(User, id=int(user_id))

    # Create a booking record for the user
    booking = ServiceBooking.objects.create(
        service=service,
        user=user,
        title=service.title,
        price=service.price,
        status='confirmed',  # Assuming the booking is confirmed after payment
        booking_date=timezone.now()
    )

    # Record the fulfillment in the Fulfillment model
    Fulfillment.objects.create(
        session_id=session_id,
        fulfilled=True
    )

    user.credits += service.credit_quantity
    user.save()
    CreditTransaction.objects.create(
        user=user,
        credits_earned=service.credit_quantity,

        log=f"Service {service.title} booked."
    )

    print(f"Service {service.title} booked for user {user.username}.")
