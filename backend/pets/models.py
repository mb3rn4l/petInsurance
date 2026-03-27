from django.db import migrations, models
from django.conf import settings

class Pet(models.Model):
    SPECIES_CHOICES = [
        ("DOG", "Dog"),
        ("CAT", "Cat"),
        ("OTHER", "Other"),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES)
    birth_date = models.DateField()
    coverage_start = models.DateField()
    coverage_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.species})"
