# authentications/urls.py
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import RegisterUser, GetUser

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),  # Endpoint for user registration
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Endpoint for obtaining JWT tokens
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # Endpoint for refreshing JWT tokens
    path('getuser/', GetUser.as_view(), name='get_user'),  # Endpoint for retrieving user details
]
