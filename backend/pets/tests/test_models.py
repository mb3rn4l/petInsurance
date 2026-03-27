import pytest
from datetime import date
from django.contrib.auth import get_user_model
from pets.models import Pet

User = get_user_model()

@pytest.mark.django_db
def test_pet_creation():
    user = User.objects.create_user(
        username='customer1', 
        email='customer1@example.com', 
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
    assert pet.name == 'Buddy'
    assert pet.species == 'DOG'
    assert str(pet) == "Buddy (DOG)"
    assert pet.owner == user
