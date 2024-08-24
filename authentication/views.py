# authentications/views.py
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication


class RegisterUser(APIView):
    def post(self, request):
        # Initialize the serializer with the request data
        serializer = UserSerializer(data=request.data)
        # Validate the data and raise an exception if invalid and save
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class GetUser(APIView):
    def get(self, request):
        JWT_authenticator = JWTAuthentication()

        # Authenticate the request and decode the JWT token
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            user, token = response  # Unpack the user and token from the response
        else:
            raise AuthenticationFailed('Unauthenticated')
        
        # Retrieve the user by ID from the token payload
        user = User.objects.filter(id=token.payload['user_id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)
    
