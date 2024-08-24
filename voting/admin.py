# voting/admin.py
from django.contrib import admin
from .models import Vote

# Registed models here.
admin.site.register(Vote)
