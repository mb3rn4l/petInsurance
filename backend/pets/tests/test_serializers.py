import pytest
from datetime import date, timedelta
from pets.serializers import PetSerializer

def test_pet_serializer_validates_coverage_end():
    today = date.today()
    data = {
        'name': 'Max',
        'species': 'CAT',
        'birth_date': '2021-05-05',
        'coverage_start': today.isoformat()
    }
    serializer = PetSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    
    validated_data = serializer.validated_data
    expected_end = today + timedelta(days=365)
    
    assert validated_data['coverage_end'] == expected_end

def test_pet_serializer_missing_required_fields():
    data = {
        'name': 'Max',
    }
    serializer = PetSerializer(data=data)
    assert not serializer.is_valid()
    assert 'species' in serializer.errors
    assert 'birth_date' in serializer.errors
    assert 'coverage_start' in serializer.errors
