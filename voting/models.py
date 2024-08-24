# voting/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from authentication.models import User
from restaurants.models import Menu

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to the user who voted
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)  # Reference to the menu item that was voted on
    voted_at = models.DateField(auto_now_add=True)  # Date when the vote was cast, automatically set to the current date
