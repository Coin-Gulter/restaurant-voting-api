import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime
from authentication.models import User
from restaurants.models import Restaurant, Menu

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_owner(db):
    return User.objects.create_user(username='owner', email='l@gmail.com', password='ownerpass')

@pytest.fixture
def create_user(db):
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def create_restaurant(db, create_owner):
    return Restaurant.objects.create(
        name='Test Restaurant',
        address='123 Test St',
        phone='1234567890',
        owner=create_owner,
        is_public=True
    )

@pytest.fixture
def create_menu(create_restaurant):
    today = datetime.now().date()
    items = {"items": ["Pizza", "Pasta", "Salad"]}
    return Menu.objects.create(restaurant=create_restaurant, date=today, items=items)

@pytest.mark.django_db
def test_menu_create(api_client, create_owner, create_restaurant):
    api_client.force_authenticate(user=create_owner)
    
    today = datetime.now().date()
    menu_data = {
        'restaurant': create_restaurant.id,
        'date': today,
        'items': {"items": ["Sushi", "Ramen"]}
    }
    
    # Valid menu creation
    response = api_client.post(reverse('upload_menu'), menu_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    
    # Attempt to create a duplicate menu for the same day
    response = api_client.post(reverse('upload_menu'), menu_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_current_day_menu(api_client, create_user, create_owner, create_menu):
    api_client.force_authenticate(user=create_user)
    
    # Retrieve today's menu (should be accessible because it's public)
    response = api_client.get(reverse('current_day_menu'))
    assert response.status_code == status.HTTP_200_OK
    results = response.json()
    assert len(results) == 1
    assert results[0]['restaurant'] == create_menu.restaurant.id

    # Change the restaurant to private and try to retrieve the menu as a different user
    create_menu.restaurant.is_public = False
    create_menu.restaurant.save()

    response = api_client.get(reverse('current_day_menu'))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    # Authenticate as the owner and retrieve the menu
    api_client.force_authenticate(user=create_owner)
    response = api_client.get(reverse('current_day_menu'))
    assert response.status_code == status.HTTP_200_OK
    results = response.json()
    assert len(results) == 1
    assert results[0]['restaurant'] == create_menu.restaurant.id
