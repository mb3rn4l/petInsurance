import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, timedelta
from pets.models import Pet
from claims.models import Claim
from claims.serializers import ClaimSerializer, ClaimReviewSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def test_user(db):
    return User.objects.create_user(
        username='cust1', 
        email='cust1@example.com', 
        password='123', 
        role='CUSTOMER'
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
def test_claim(test_user, test_pet, db):
    return Claim.objects.create(
        owner=test_user,
        pet=test_pet,
        invoice='invoices/test.pdf',
        invoice_hash='abc123hash_rev',
        invoice_date=date(2023, 5, 5),
        date_of_event=date(2023, 5, 1),
        amount=150.00,
        status='IN_REVIEW'
    )

@pytest.mark.django_db
def test_claim_serializer_validates_amount_and_date(test_pet):
    # Valid data
    valid_file = SimpleUploadedFile("invoice.pdf", b"fake file content", content_type="application/pdf")
    data = {
        'pet': test_pet.id,
        'invoice': valid_file,
        'invoice_date': '2023-05-01',
        'date_of_event': '2023-04-28',
        'amount': '100.00'
    }
    serializer = ClaimSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

    # Invalid date (outside coverage)
    data_date_invalid = data.copy()
    data_date_invalid['invoice_date'] = '2022-12-31'
    serializer_date = ClaimSerializer(data=data_date_invalid)
    assert not serializer_date.is_valid()
    assert 'invoice_date' in serializer_date.errors

    # Invalid amount
    data_amount_invalid = data.copy()
    data_amount_invalid['amount'] = '-10.00'
    serializer_amount = ClaimSerializer(data=data_amount_invalid)
    assert not serializer_amount.is_valid()
    assert 'amount' in serializer_amount.errors

@pytest.mark.django_db
def test_claim_serializer_duplicate_invoice_hash(test_pet, test_user):
    # First claim saves an invoice
    valid_file1 = SimpleUploadedFile("inv1.pdf", b"same content", content_type="application/pdf")
    data1 = {
        'pet': test_pet.id,
        'invoice': valid_file1,
        'invoice_date': '2023-05-01',
        'date_of_event': '2023-04-28',
        'amount': '100.00'
    }
    serializer1 = ClaimSerializer(data=data1)
    assert serializer1.is_valid(), serializer1.errors
    # simulate the view saving it manually to bypass the request.user logic tests
    serializer1.save(owner=test_user, invoice_hash=getattr(serializer1, 'calculated_hash', ''))

    # Second claim tries to use same file content -> same hash
    valid_file2 = SimpleUploadedFile("inv2.pdf", b"same content", content_type="application/pdf")
    data2 = {
        'pet': test_pet.id,
        'invoice': valid_file2,
        'invoice_date': '2023-06-01',
        'date_of_event': '2023-05-28',
        'amount': '50.00'
    }
    serializer2 = ClaimSerializer(data=data2)
    assert not serializer2.is_valid()
    assert 'invoice' in serializer2.errors
    assert "already been registered" in str(serializer2.errors['invoice'])

@pytest.mark.django_db
def test_claim_review_serializer_requires_in_review(test_claim):
    # Change status to PROCESSING
    test_claim.status = 'PROCESSING'
    test_claim.save()
    
    data = {'status': 'APPROVED'}
    serializer = ClaimReviewSerializer(test_claim, data=data)
    assert not serializer.is_valid()
    assert "Only claims in IN_REVIEW status can be reviewed." in serializer.errors['non_field_errors']

@pytest.mark.django_db
def test_claim_review_serializer_requires_notes_on_rejection(test_claim):
    # test_claim is already IN_REVIEW
    data = {'status': 'REJECTED', 'review_notes': ''}
    serializer = ClaimReviewSerializer(test_claim, data=data)
    assert not serializer.is_valid()
    assert 'review_notes' in serializer.errors

    data_with_notes = {'status': 'REJECTED', 'review_notes': 'Not covered.'}
    serializer2 = ClaimReviewSerializer(test_claim, data=data_with_notes)
    assert serializer2.is_valid()
