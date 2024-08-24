# restaurants/serializers.py
from rest_framework import serializers
from .models import Restaurant, Menu

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone', 'description', 'owner', 'is_public']  # include in the serialized data
        read_only_fields = ['id', 'owner']  # (not editable)

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'date', 'items']  # include in the serialized data
        read_only_fields = ['id']  # (not editable)
