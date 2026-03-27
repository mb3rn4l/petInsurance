from django.db import models
from django.conf import settings
from pets.models import Pet

class Claim(models.Model):
    STATUS_CHOICES = [
        ("PROCESSING", "Processing"),
        ("IN_REVIEW", "In Review"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='claims')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='claims')
    invoice = models.FileField(upload_to="invoices/")
    invoice_hash = models.CharField(max_length=255, unique=True)
    invoice_date = models.DateField()
    date_of_event = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PROCESSING")
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_claims')
    review_notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim #{self.id} for {self.pet.name} - {self.status}"
