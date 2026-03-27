import pytest
from datetime import date
from django.contrib.auth import get_user_model
from pets.models import Pet
from claims.models import Claim

User = get_user_model()

@pytest.mark.django_db
def test_claim_str_representation():
    user = User.objects.create_user(
        username='customer_claim', 
        email='custc@example.com', 
        password='password123', 
        role='CUSTOMER'
    )
    pet = Pet.objects.create(
        owner=user,
        name='Buddy',
        species='DOG',
        birth_date=date(2020, 1, 1),
        coverage_start=date(2023, 1, 1),
        coverage_end=date(2024, 1, 1),
    )
    claim = Claim.objects.create(
        owner=user,
        pet=pet,
        invoice='invoices/test.pdf',
        invoice_hash='abc123hash',
        invoice_date=date(2023, 5, 5),
        date_of_event=date(2023, 5, 1),
        amount=150.00,
        status='PROCESSING'
    )
    assert str(claim) == f"Claim #{claim.id} for Buddy - PROCESSING"
