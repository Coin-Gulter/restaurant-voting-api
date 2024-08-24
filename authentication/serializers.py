# authentication/serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password'] 
        extra_kwargs = {
            'password': {'write_only': True}  # Ensure the password is write-only (not readable in responses)
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)  # Extract the password from validated data
        instance = self.Meta.model(**validated_data)  # Create a new instance of the User model
        if password is not None:
            instance.set_password(password)  # Hash the password before saving
        instance.save()  # Save the user instance to the database
        return instance
