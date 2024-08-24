# voting/serializers.py
from rest_framework import serializers
from .models import Vote

class VoteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display the user as a string (e.g., username) instead of an ID
    menu = serializers.StringRelatedField()  # Display the menu as a string (e.g., menu details) instead of an ID

    class Meta:
        model = Vote
        fields = ['id', 'user', 'menu', 'voted_at']  # Fields to include in the serialized data
