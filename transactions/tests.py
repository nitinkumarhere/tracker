from django.test import TestCase

# Create your tests here.
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from categories.models import Category
from transactions.models import Transaction
import datetime

User = get_user_model()


@pytest.fixture
def auth_client():
    user = User.objects.create_user(email="owner@example.com", name="Owner", password="password123")
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user


@pytest.fixture
def secondary_user():
    return User.objects.create_user(email="stranger@example.com", name="Stranger", password="password123")


@pytest.mark.django_db
class TestTransactionsAPI:

    def test_create_transaction_and_isolation(self, auth_client, secondary_user):
        client, user = auth_client
        category = Category.objects.create(name="Food", is_default=True)

        url = reverse('transaction-list')
        payload = {
            "amount": "45.50",
            "type": "EXPENSE",
            "category": category.id,
            "date": str(datetime.date.today()),
            "note": "Dinner out"
        }

        # 1. Create a transaction for the authenticated user
        response = client.post(url, payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        tx_id = response.data['id']

        # 2. Verify owner can fetch it
        assert Transaction.objects.filter(user=user).count() == 1

        # 3. Verify a different user cannot access or view this transaction details
        client.force_authenticate(user=secondary_user)
        detail_url = reverse('transaction-detail', kwargs={'pk': tx_id})
        get_response = client.get(detail_url)
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
