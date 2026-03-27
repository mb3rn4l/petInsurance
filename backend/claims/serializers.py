from rest_framework import serializers
from .models import Claim
import hashlib

def generate_file_hash(file):
    hasher = hashlib.sha256()
    for chunk in file.chunks():
        hasher.update(chunk)
    return hasher.hexdigest()

class ClaimSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    invoice_hash = serializers.CharField(read_only=True)
    pet_name = serializers.CharField(source='pet.name', read_only=True)

    class Meta:
        model = Claim
        fields = (
            'id', 'owner', 'pet', 'pet_name', 'invoice',
            'invoice_hash', 'invoice_date', 'date_of_event',
            'amount', 'status', 'reviewer', 'review_notes', 'created_at'
        )
        read_only_fields = ('status', 'reviewer', 'review_notes', 'invoice_hash')

    def validate(self, data):
        pet = data["pet"]
        invoice_date = data["invoice_date"]
        invoice_file = data.get("invoice")

        if not (pet.coverage_start <= invoice_date <= pet.coverage_end):
            raise serializers.ValidationError({
                "invoice_date": "The invoice date is outside the pet's coverage period."
            })

        if data.get("amount", 0) <= 0:
            raise serializers.ValidationError({
                "amount": "The claim amount must be greater than zero."
            })

        if invoice_file:
            invoice_hash = generate_file_hash(invoice_file)
            if Claim.objects.filter(invoice_hash=invoice_hash).exists():
                raise serializers.ValidationError({
                    "invoice": "This invoice has already been registered in another claim."
                })
            self.calculated_hash = invoice_hash

        return data


class ClaimReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Claim
        fields = ('status', 'review_notes')

    def validate(self, data):
        claim = self.instance
        if claim.status != 'IN_REVIEW':
            raise serializers.ValidationError(
                "Only claims in IN_REVIEW status can be reviewed."
            )

        new_status = data.get('status')
        if new_status not in ('APPROVED', 'REJECTED'):
            raise serializers.ValidationError({
                "status": "The status must be APPROVED or REJECTED."
            })

        if new_status == 'REJECTED' and not data.get('review_notes'):
            raise serializers.ValidationError({
                "review_notes": "Review notes are required when rejecting a claim."
            })

        return data
