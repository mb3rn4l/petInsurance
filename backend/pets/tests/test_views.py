import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from pets.models import Pet
from datetime import date

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def customer_user(db):
    user = User.objects.create_user(username='customer', email='cust@example.com', password='pass', role='CUSTOMER')
    return user

@pytest.fixture
def admin_user(db):
    user = User.objects.create_user(username='admin', email='adm@example.com', password='pass', role='ADMIN')
    return user

@pytest.fixture
def other_customer_user(db):
    user = User.objects.create_user(username='customer2', email='cust2@example.com', password='pass', role='CUSTOMER')
    return user

@pytest.fixture
def pet(customer_user, db):
    return Pet.objects.create(
        owner=customer_user,
        name='Buddy',
        species='DOG',
        birth_date=date(2020, 1, 1),
        coverage_start=date(2023, 1, 1),
        coverage_end=date(2024, 1, 1)
    )

@pytest.mark.django_db
def test_get_pets_unauthenticated(api_client):
    url = reverse('pet-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_get_pets_as_customer(api_client, customer_user, pet):
    api_client.force_authenticate(user=customer_user)
    url = reverse('pet-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Buddy'

@pytest.mark.django_db
def test_get_pets_isolates_by_owner(api_client, other_customer_user, pet):
    api_client.force_authenticate(user=other_customer_user)
    url = reverse('pet-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0

@pytest.mark.django_db
def test_create_pet_as_customer(api_client, customer_user):
    api_client.force_authenticate(user=customer_user)
    url = reverse('pet-list')
    data = {
        'name': 'Bella',
        'species': 'CAT',
        'birth_date': '2019-02-14',
        'coverage_start': date.today().isoformat()
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Pet.objects.count() == 1
    
    new_pet = Pet.objects.first()
    assert new_pet.owner == customer_user
    assert new_pet.name == 'Bella'

