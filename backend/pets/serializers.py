from rest_framework import serializers
from .models import Pet
from datetime import timedelta

class PetSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    coverage_end = serializers.DateField(read_only=True)

    class Meta:
        model = Pet
        fields = (
            'id', 'owner', 'name', 'species', 
            'birth_date', 'coverage_start', 
            'coverage_end', 'created_at'
        )

    def validate(self, data):
        # The backend automatically calculates the coverage end date
        if 'coverage_start' in data:
            data['coverage_end'] = data['coverage_start'] + timedelta(days=365)
        return data
