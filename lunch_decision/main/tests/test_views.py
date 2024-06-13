import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from main.models import Restaurant, Menu, Vote
import main.models


import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_jwt.settings import api_settings

@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="password")

@pytest.fixture
def api_client(user):
    client = APIClient()
    payload = api_settings.JWT_PAYLOAD_HANDLER(user)
    token = api_settings.JWT_ENCODE_HANDLER(payload)
    client.credentials(HTTP_AUTHORIZATION="JWT " + token)
    return client

@pytest.mark.django_db
def test_create_restaurant(api_client):
    response = api_client.post("/main/restaurant/create-restaurant/", {"name": "Test Restaurant"})
    assert response.status_code == 201
    response = api_client.post("/main/restaurant/create-restaurant/", {"someley": "notValid"})
    assert response.status_code == 400


@pytest.mark.django_db
def test_upload_menu_and_get_current_day_menu(api_client):
    restaurant = Restaurant.objects.create(name= "Test Restaurant")
    data = {
        "restaurant": restaurant.id,
        "date": timezone.localdate(),
        "items": [
            {"name": "Item 1", "price": 10.00},
            {"name": "Item 2", "price": 15.00},
        ]
    }
    response = api_client.post("/main/menu/upload-menu/", data, format="json" ,follow=True)
    assert response.status_code == 201
    assert "items" in response.data
    assert len(response.data["items"]) == 2

    invalid_case = {
        "restaurant": 100,
        "date": timezone.localdate(),
        "items": [
            {"name": "Item 1", "price": 10.00},
            {"name": "Item 2", "price": 15.00},
        ]
    }

    response = api_client.post("/main/menu/upload-menu/", invalid_case, format="json")
    assert response.status_code == 404

### get current day menu 
    response = api_client.get("/main/menu/current-day-menu/")
    assert response.status_code == 200
    assert "items" in response.data[0]
    assert len(response.data) == 1


@pytest.mark.django_db
def test_create_user(api_client):
    data = {"name": "test user"}
    response = api_client.post("/main/user/create-user/", data)
    assert response.status_code == 201
