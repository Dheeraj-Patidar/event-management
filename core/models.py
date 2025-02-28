from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

from .managers import UserManager


class User(AbstractUser):
    ROLE_CHOICES = (("admin", "ADMIN"), ("student", "STUDENT"), ("staff", "STAFF"))

    first_name = models.CharField(max_length=100, default=None, null=True)
    last_name = models.CharField(max_length=100, default=None, null=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=100, default=None, null=True)
    username = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100, default=None, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="admin")

    objects = UserManager()


class EventManager(models.Manager):
    def get_queryset(self):
        """Automatically update expired status when fetching events."""
        events = super().get_queryset()
        events.filter(date__lt=now(), expired=False).update(expired=True)
        return events


class Event(models.Model):
    event_name = models.CharField(max_length=255, default=None, null=True)
    description = models.CharField(max_length=150, default=None, null=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=255, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired = models.BooleanField(default=False)

    objects = EventManager()

    def save(self, *args, **kwargs):
        self.expired = self.date < now()
        super().save(*args, **kwargs)


class RegisteredStudent(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=None, null=True)
    first_name = models.CharField(max_length=100, default=None, null=True)
    last_name = models.CharField(max_length=100, default=None, null=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=100, default=None, null=True)
    enrolled_date = models.DateField(auto_now_add=True)

