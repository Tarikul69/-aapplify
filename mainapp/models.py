from django.db import models
from django.utils.translation import gettext as _
from authentication.models import User, BaseModel

# class Ticket(BaseModel):
#     name = models.CharField(_("Ticket Name"), max_length=50)

#     def __str__(self):
#         return self.name

class Ticket(BaseModel):
    name = models.CharField(_("Ticket Name"), max_length=50)
    staff = models.OneToOneField('authentication.User', on_delete=models.CASCADE, related_name='staff', null=True, blank=True)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name="user")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")




class Message(BaseModel):
    room = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name="user_messages")
    staff = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, null=True, blank=True, related_name="staff_responses")
    content = models.TextField(_("Message Content"))
    is_staff_response = models.BooleanField(default=False)

    def __str__(self):
        if self.is_staff_response:
            return f"Staff Response in Room {self.room.room_number} by {self.staff.user.email}"
        return f"User Message in Room {self.room.room_number} by {self.user.email}"

    def __str__(self):
        sender = self.staff.user.email if self.staff else self.user.email
        sender_type = "Staff" if self.staff else "User"
        return f"{sender_type} Message in Room {self.room.room_number} by {sender}"

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ['-pk']

class Images(BaseModel):
    message = models.ForeignKey(Message, verbose_name=_("messages"), on_delete=models.CASCADE)
    image = models.ImageField(_(""), upload_to=None, height_field=None, width_field=None, max_length=None)

# class Service(BaseModel):
