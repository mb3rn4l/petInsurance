import threading
# import time

from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Claim
from .serializers import ClaimSerializer, ClaimReviewSerializer
from .utils import process_claim_async
from accounts.permissions import IsCustomer, IsSupport, IsAdmin


class ClaimViewSet(viewsets.GenericViewSet, 
                    mixins.ListModelMixin, 
                    mixins.CreateModelMixin, 
                    mixins.RetrieveModelMixin):
    serializer_class = ClaimSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomer]

    def get_queryset(self):
        user = self.request.user
        # Base queryset by rol 
        if user.role in ['SUPPORT', 'ADMIN']:
            qs = Claim.objects.all()
        else:
            qs = Claim.objects.filter(owner=user)

        # Optional filter by status via query param 
        status_filter = self.request.query_params.get('status')
        valid_statuses = {'PROCESSING', 'IN_REVIEW', 'APPROVED', 'REJECTED'}
        if status_filter and status_filter in valid_statuses:
            qs = qs.filter(status=status_filter)

        return qs.order_by('-created_at')

    def perform_create(self, serializer):
        pet = serializer.validated_data['pet']
        if pet.owner != self.request.user:
            raise PermissionDenied("You cannot register a claim for a pet that does not belong to you.")

        claim = serializer.save(
            owner=self.request.user,
            invoice_hash=getattr(serializer, 'calculated_hash', None)
        )

        # Disparar procesamiento asíncrono (Feature 4)
        thread = threading.Thread(target=process_claim_async, args=(claim.id,))
        thread.daemon = True
        thread.start()

    @action(detail=False, methods=['get'], url_path='review', permission_classes=[IsSupport | IsAdmin])
    def review_list(self, request):
        queryset = Claim.objects.filter(status='IN_REVIEW').select_related('pet', 'owner').order_by('-created_at')
        serializer = ClaimSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='review', permission_classes=[IsSupport | IsAdmin])
    def review(self, request, pk=None):
        claim = self.get_object()
        serializer = ClaimReviewSerializer(claim, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save(reviewer=request.user)
            return Response(ClaimSerializer(claim).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
