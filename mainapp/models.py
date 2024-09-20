from django.db import models
from django.utils.translation import gettext as _
from authentication.models import User, BaseModel
from slugify import slugify
from django_ckeditor_5.fields import CKEditor5Field



# class Ticket(BaseModel):
#     name = models.CharField(_("Ticket Name"), max_length=50)

#     def __str__(self):
#         return self.name

class Ticket(BaseModel):
    subject = models.CharField(_("Subject"), max_length=255)
    staff = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='staffs', null=True, blank=True)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name="users", null=True, blank=True)

    def __str__(self):
        return f"#Ticket{self.pk}"

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")

class Message(BaseModel):
    room = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name="message_users")
    # content = models.TextField(_("Message Content"))
    content = CKEditor5Field('Text', config_name='extends')
    is_staff_response = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ['-pk']

class Images(BaseModel):
    message = models.ForeignKey(Message, verbose_name=_("messages"), on_delete=models.CASCADE)
    image = models.ImageField(_(""), upload_to='message_img/', height_field=None, width_field=None, max_length=None)

class Service(BaseModel):
    title = models.CharField(_("Title"), max_length=255)
    short_description = models.TextField(_("Short Description"))
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    thumbnail_img = models.ImageField(_("Thumbnail Image"), upload_to='thumbnails/', height_field=None, width_field=None, max_length=None)
    description = models.TextField(_("Description"))

    def __str__(self):
        return self.title

class ServiceBooking(BaseModel):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='service_bookings')
    booking_date = models.DateTimeField(_("Booking Date"), auto_now_add=True)
    status = models.CharField(_("Status"), max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    title = models.CharField(_("Title"), max_length=255)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user} - {self.service.title} ({self.get_status_display()})"

class Payment(BaseModel):
    booking = models.OneToOneField(ServiceBooking, on_delete=models.CASCADE, related_name="payment")
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name="payments")
    stripe_payment_intent_id = models.CharField(_("Stripe Payment Intent ID"), max_length=255)
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)
    currency = models.CharField(_("Currency"), max_length=10, default="usd")
    status = models.CharField(_("Payment Status"), max_length=20, choices=[
        ('pending', 'Pending'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
    ], default='pending')
    created_at = models.DateTimeField(_("Payment Date"), auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.booking.service.title} by {self.user}"

class BlogPost(BaseModel):
    title = models.CharField(_("Blog Title"), max_length=255, unique=True)
    slug = models.SlugField(_("Blog Slug"), unique=True)
    thumbnail = models.ImageField(_("Blog Thumbnail"), upload_to='blog/')
    created_by = models.ForeignKey("authentication.User", verbose_name=_("Created By The User"), on_delete=models.CASCADE)
    # body = models.TextField(_("Main Body"))
    body = CKEditor5Field('Text', config_name='extends')
    is_accepted = models.BooleanField(_("Blog accepted"), default=False)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)
