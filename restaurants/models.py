# restaurants/models.py
from django.db import models
from django.conf import settings  # Import settings to access AUTH_USER_MODEL

class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Name of the restaurant, must be unique
    address = models.CharField(max_length=255)  # Address of the restaurant
    phone = models.CharField(max_length=20)  # Phone number of the restaurant
    description = models.TextField(blank=True, null=True)  # Optional description of the restaurant
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='restaurants', on_delete=models.CASCADE)  # Reference to the user who owns the restaurant
    is_public = models.BooleanField(default=False)  # Field to indicate if the restaurant is public

    def __str__(self):
        return self.name

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='menus', on_delete=models.CASCADE)  # Reference to the associated restaurant
    date = models.DateField()  # Date for the menu
    items = models.JSONField()  # JSONField to store a list of menu items with details

    def __str__(self):
        return f"{self.restaurant.name} - {self.date}"


