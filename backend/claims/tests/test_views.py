import pytest
from unittest.mock import patch
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from pets.models import Pet
from claims.models import Claim
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        username='c_claim_views', 
        email='clm@cx.com', 
        password='123', 
        role='CUSTOMER'
    )

@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        username='other_claim_views', 
        email='other@cx.com', 
        password='123', 
        role='CUSTOMER'
    )

@pytest.fixture
def support_user(db):
    return User.objects.create_user(
        username='supp_claim_views', 
        email='sup@cx.com', 
        password='123', 
        role='SUPPORT'
    )

@pytest.fixture
def test_pet(test_user, db):
    return Pet.objects.create(
        owner=test_user,
        name='Max',
        species='CAT',
        birth_date=date(2020, 1, 1),
        coverage_start=date(2023, 1, 1),
        coverage_end=date(2024, 1, 1)
    )

@pytest.fixture
def other_pet(other_user, db):
    return Pet.objects.create(
        owner=other_user,
        name='OtherPet',
        species='DOG',
        birth_date=date(2020, 1, 1),
        coverage_start=date(2023, 1, 1),
        coverage_end=date(2024, 1, 1)
    )

@pytest.fixture
def test_claim(test_user, test_pet, db):
    return Claim.objects.create(
        owner=test_user,
        pet=test_pet,
        invoice='invoices/test.pdf',
        invoice_hash='hash_view_claim_123',
        invoice_date=date(2023, 5, 5),
        date_of_event=date(2023, 5, 1),
        amount=150.00,
        status='IN_REVIEW'
    )

@pytest.mark.django_db
def test_get_claims_lists_owners_claims_only(api_client, test_user, other_user, test_claim):
    api_client.force_authenticate(user=test_user)
    url = reverse('claim-list')
    res = api_client.get(url)
    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1
    
    api_client.force_authenticate(user=other_user)
    res2 = api_client.get(url)
    assert res2.status_code == status.HTTP_200_OK
    assert len(res2.data) == 0

@pytest.mark.django_db
@patch('claims.views.threading.Thread')
def test_create_claim_valid(mock_thread, api_client, test_user, test_pet):
    api_client.force_authenticate(user=test_user)
    url = reverse('claim-list')
    valid_file = SimpleUploadedFile(
        "invoice_views.pdf", 
        b"fake file content views", 
        content_type="application/pdf"
    )
    data = {
        'pet': test_pet.id,
        'invoice': valid_file,
        'invoice_date': '2023-05-01',
        'date_of_event': '2023-04-28',
        'amount': '100.00'
    }
    
    res = api_client.post(url, data, format='multipart')
    assert res.status_code == status.HTTP_201_CREATED
    assert Claim.objects.count() == 1
    
    mock_thread.assert_called_once()
    mock_thread_instance = mock_thread.return_value
    mock_thread_instance.start.assert_called_once()

@pytest.mark.django_db
def test_create_claim_for_other_users_pet_fails(api_client, test_user, other_pet):
    api_client.force_authenticate(user=test_user)
    url = reverse('claim-list')
    valid_file = SimpleUploadedFile(
        "invoice_views2.pdf", 
        b"fake file content views 2", 
        content_type="application/pdf"
    )
    data = {
        'pet': other_pet.id,
        'invoice': valid_file,
        'invoice_date': '2023-05-01',
        'date_of_event': '2023-04-28',
        'amount': '100.00'
    }
    res = api_client.post(url, data, format='multipart')
    assert res.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_review_list_accessible_to_support(api_client, support_user, test_claim):
    api_client.force_authenticate(user=support_user)
    url = reverse('claim-review-list')
    res = api_client.get(url)
    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1
    assert res.data[0]['status'] == 'IN_REVIEW'

@pytest.mark.django_db
def test_review_claim_as_support(api_client, support_user, test_claim):
    api_client.force_authenticate(user=support_user)
    url = reverse('claim-review', kwargs={'pk': test_claim.id})
    data = {'status': 'APPROVED'}
    res = api_client.post(url, data)
    assert res.status_code == status.HTTP_200_OK
    
    test_claim.refresh_from_db()
    assert test_claim.status == 'APPROVED'
    assert test_claim.reviewer == support_user

@pytest.mark.django_db
def test_review_claim_as_customer_fails(api_client, test_user, test_claim):
    api_client.force_authenticate(user=test_user)
    # The URL to POST a review
    url = reverse('claim-review', kwargs={'pk': test_claim.id})
    data = {'status': 'APPROVED'}
    res = api_client.post(url, data)
    assert res.status_code == status.HTTP_403_FORBIDDEN
