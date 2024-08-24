# restaurants/views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from datetime import datetime
from django.db.models import Q
from .models import Restaurant, Menu
from .serializers import RestaurantSerializer, MenuSerializer

# Custom permission to check if the user is the restaurant owner or an admin
class IsOwnerOrAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        # Grant access if the user is an admin or the owner of the restaurant
        return request.user.is_staff or obj.owner == request.user

# Create Restaurant
class RestaurantCreateView(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsOwnerOrAdmin]  # Ensure only authenticated users owner or admin have access

    def perform_create(self, serializer):
        # Check if a restaurant with the same name already exists
        if Restaurant.objects.filter(name=serializer.validated_data['name']).exists():
            raise ValidationError(f"Restaurant '{serializer.validated_data['name']}' already exists.")
        # Save the restaurant with the current user as the owner
        serializer.save(owner=self.request.user)

# Upload Menu
class MenuCreateView(generics.CreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsOwnerOrAdmin]   # Ensure only authenticated users owner or admin have access

    def perform_create(self, serializer):
        restaurant = serializer.validated_data['restaurant']
        # Check if a menu for this restaurant on this date already exists
        if Menu.objects.filter(restaurant=restaurant, date=serializer.validated_data['date']).exists():
            raise ValidationError(f"Menu for '{restaurant.name}' on {serializer.validated_data['date']}' already exists.")
        # Save the menu
        serializer.save()

# Get Current Day Menu
class CurrentDayMenuView(generics.ListAPIView):
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def get_queryset(self):
        today = datetime.now().date()  # Get today's date
        user = self.request.user
        # Filter menus for today that are either owned by the user or public
        return Menu.objects.filter(
            Q(date=today) & (Q(restaurant__owner=user) | Q(restaurant__is_public=True))
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            # Return a 404 response if no menus are available
            return Response({"detail": "No menus available today."}, status=status.HTTP_404_NOT_FOUND)
        return super().list(request, *args, **kwargs)
