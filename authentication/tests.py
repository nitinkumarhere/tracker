from django.test import TestCase

# Create your tests here.
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestAuthenticationAPI:

    def test_user_registration_success(self, client):
        url = reverse('auth_register')
        payload = {
            "email": "testuser@example.com",
            "name": "Test User",
            "password": "securepassword123"
        }
        response = client.post(url, payload, content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['email'] == "testuser@example.com"
        assert 'password' not in response.data

    def test_user_login_and_jwt_generation(self, client):
        # Setup initial profile
        User.objects.create_user(email="login@example.com", name="User", password="password123")

        url = reverse('token_obtain_pair')
        payload = {"email": "login@example.com", "password": "password123"}
        response = client.post(url, payload, content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
