from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (("admin", "ADMIN"), ("student", "STUDENT"), ("staff", "STAFF"))

    first_name = models.CharField(max_length=100, default=None, null=True)
    last_name = models.CharField(max_length=100, default=None, null=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=100, default=None, null=True)
    username = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100, default=None, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="admin")
