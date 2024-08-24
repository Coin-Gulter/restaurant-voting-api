# Authentication/admin.py
from django.contrib import admin
from .models import User

# Registed models
admin.site.register(User)
