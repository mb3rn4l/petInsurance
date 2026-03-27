from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Pet
from .serializers import PetSerializer
from accounts.permissions import IsCustomer

class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
