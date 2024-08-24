# authentication/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Additional fields for the custom user model
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  # (hashed in practice)