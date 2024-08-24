# restaurants/admin.py
from django.contrib import admin
from .models import Restaurant, Menu

# Registed models here.
admin.site.register([Restaurant, Menu])
