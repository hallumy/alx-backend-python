from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

class CustomUser(AbstractUser):
    """
    Custom User model extending Django AbstracatUser and overrides the email attribute.
    Adds:
    - phone_number : optional phone number
    - role: user role with fixed choice
    - created_at: Timestamp when the user account was created.

    Inherits all default fields like username, password, fname, lname .
    """
    ROLES = [
        ('guest', _('Guest')),
        ('host', _('Host')),
        ('admin', _('Admin')),
    ]
    email        = models.EmailField(unique=True)
    phone_number = models.CharField(max_length = 20, blank = True, null=True)
    role         = models.CharField(blank=True, choices=ROLES, default='guest')
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the user
        """
        return f"{self.username} ({self.role})"

class Conversation(models.Model):
    """
    Represents a one on one or group conversation between users.
    participants_id references to a user participating in the conversation.
    created_at is the timestamp when the conversation is created
    """
    participants_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at      = models.DateTimeField(auto_add_now=True)

class Message(models.Model):
    """
    Represents the message being sent between users
    sender_id is a reference to the user sending the message
    message_body contains the message field to be sent
    sent_at is the timestamp when the message is sent
    """
    sender_id       = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message_body    = models.TextField(null=False)
    sent_at         = models.DateTimeField(auto_addd_now=True)