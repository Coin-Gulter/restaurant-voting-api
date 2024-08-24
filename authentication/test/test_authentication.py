import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_user_registration(api_client):
    # Test data for user registration
    user_data = {
        'username': 'newuser',
        'password': 'newpassword',
        'email': 'newuser@example.com',
        'name': 'New User'
    }
    
    # Register a new user
    response = api_client.post(reverse('register'), user_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    
    # Verify the user was created in the database
    assert User.objects.filter(username='newuser').exists()

@pytest.mark.django_db
def test_token_obtain_pair(api_client, create_user):
    # Obtain JWT token with correct credentials
    response = api_client.post(reverse('token_obtain_pair'), {
        'username': create_user.username,
        'password': 'testpass'
    }, format='json')
    
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data
    
    assert response.data['access'], response.data['refresh']

@pytest.mark.django_db
def test_token_refresh(api_client, create_user):
    # Obtain JWT token with correct credentials
    response = api_client.post(reverse('token_obtain_pair'), {
        'username': create_user.username,
        'password': 'testpass'
    }, format='json')
    
    refresh_token = response.data['refresh']
    
    # Refresh the JWT token
    response = api_client.post(reverse('token_refresh'), {
        'refresh': refresh_token
    }, format='json')
    
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data

@pytest.mark.django_db
def test_get_user(api_client, create_user):
    # Obtain JWT token with correct credentials
    response = api_client.post(reverse('token_obtain_pair'), {
        'username': create_user.username,
        'password': 'testpass'
    }, format='json')

    access_token = response.data['access']
    
    # Use the access token to authenticate the request
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.get(reverse('get_user'))
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == create_user.username

@pytest.fixture
def create_user(db):
    return User.objects.create_user(username='testuser', password='testpass')
