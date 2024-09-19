from django.core.mail import send_mail
from django.core.mail import EmailMessage

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

def email_sender(user_email, message, subject="Aapplify app password"):
    send_mail(
        subject,
        message,
        'fff147570@gmail.com',
        [user_email],
        fail_silently=False,
    )


def password_set_email(user):
    email = user.email
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    reset_link = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
    
    subject = 'Set your new password'
    message = render_to_string('account/password_reset_email.html', {
        'user': user,
        'reset_link': f"https://server.basepapers.co{reset_link}",
    })
    
    # Send the email
    my_email = "fff147570@gmail.com"
    email_message = EmailMessage(
        subject,
        message,
        my_email,
        [email],
    )
    email_message.content_subtype = 'html'  # This is important to render the message as HTML
    email_message.send(fail_silently=False)
