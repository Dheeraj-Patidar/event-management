from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role=(
        ('admin','ADMIN'),
        ('student','STUDENT'),
        ('staff','STAFF')
    )

    first_name=models.CharField(max_length=100,default=None,null=True)
    last_name=models.CharField(max_length=100,default=None,null=True)
    email=models.EmailField(max_length=100,unique=True)
    phone_number=models.CharField(max_length=100,default=None,null=True)
    password=models.CharField(max_length=100,default=None,null=True)
    role=models.CharField(max_length=50,choices=role,default='admin')

