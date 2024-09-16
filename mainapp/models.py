from django.db import models
from django.utils.translation import gettext as _
from authentication.models import User, Staff, BaseModel

class Room(BaseModel):
    room_name = models.CharField(_("Room Number"), max_length=50)
    staff = models.OneToOneField('authentication.Staff', on_delete=models.CASCADE, related_name='staff', null=True, blank=True)
    regular = models.ForeignKey('authentication.RegularUser', on_delete=models.CASCADE, related_name="user_messages")

    def __str__(self):
        return self.room_name

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")


class Message(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey('authentication.RegularUser', on_delete=models.CASCADE, related_name="user_messages")
    staff = models.ForeignKey('authentication.Staff', on_delete=models.SET_NULL, null=True, blank=True, related_name="staff_responses")
    content = models.TextField(_("Message Content"))
    timestamp = models.DateTimeField(auto_now_add=True)
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
        ordering = ['-timestamp']
