import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import datetime
from authentication.models import User
from restaurants.models import Restaurant, Menu
from voting.models import Vote

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def create_owner(db):
    return User.objects.create_user(username='owner', email="k@gmail.com", password='ownerpass')

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
    items = {"items": ["Pizza", "Pasta", "Salad"]}
    date = datetime.now().date()
    return Menu.objects.create(restaurant=create_restaurant, date=date, items=items)

@pytest.mark.django_db
def test_vote_create(api_client, create_user, create_menu):
    api_client.force_authenticate(user=create_user)
    today_new = datetime.now().date()

    # Valid vote creation
    response = api_client.post(reverse('vote'), {'menu_id': create_menu.id})
    assert response.status_code == status.HTTP_201_CREATED

    # Verify the vote was created
    assert Vote.objects.filter(user=create_user, voted_at=today_new).exists()

    # Duplicate vote for the same day
    response = api_client.post(reverse('vote'), {'menu_id': create_menu.id})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_voting_results(api_client, create_user, create_menu):
    api_client.force_authenticate(user=create_user)

    # Cast a vote
    api_client.post(reverse('vote'), {'menu_id': create_menu.id})

    # Retrieve today's voting results
    response = api_client.get(reverse('voting-results'))
    assert response.status_code == status.HTTP_200_OK

    results = response.json()
    print(results)
    assert len(results) == 1
    assert results[0]['menu__restaurant__name'] == create_menu.restaurant.name
    assert results[0]['vote_count'] == 1
