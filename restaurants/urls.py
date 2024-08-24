# restaurants/urls.py
from django.urls import path
from .views import RestaurantCreateView, MenuCreateView, CurrentDayMenuView

urlpatterns = [
    path('create/', RestaurantCreateView.as_view(), name='create_restaurant'),  # Endpoint for creating a new restaurant
    path('menus/', MenuCreateView.as_view(), name='upload_menu'),  # Endpoint for uploading a menu
    path('menus/today/', CurrentDayMenuView.as_view(), name='current_day_menu'),  # Endpoint for retrieving the menu for the current day
]
