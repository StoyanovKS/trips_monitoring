from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class Car(models.Model):
    class FuelChoices(models.TextChoices):
        PETROL = "petrol", "Petrol"
        DIESEL = "diesel", "Diesel"
        HYBRID = "hybrid", "Hybrid"
        ELECTRIC = "electric", "Electric"
        LPG = "lpg", "LPG"
        CNG = "cng", "CNG"

    class GearboxChoices(models.TextChoices):
        MANUAL = "manual", "Manual"
        AUTOMATIC = "automatic", "Automatic"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cars",
    )

    brand = models.CharField(max_length=40)
    model = models.CharField(max_length=60)

    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1950),
            MaxValueValidator(timezone.now().year + 1),
        ]
    )

    fuel = models.CharField(
        max_length=16,
        choices=FuelChoices.choices,
    )

    gearbox = models.CharField(
        max_length=16,
        choices=GearboxChoices.choices,
    )

    vin = models.CharField(
        max_length=17,
        blank=True,
        null=True,
        help_text="Optional. VIN is 17 characters.",
    )

    photo = models.ImageField(
        upload_to="cars/",
        blank=True,
        null=True,
    )

    # Second M2M to Tag lives here, Tag model is in logbook app
    tags = models.ManyToManyField(
        "logbook.Tag",
        blank=True,
        related_name="cars",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("owner", "brand", "model", "year")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

    def clean(self):
        super().clean()

        if self.vin:
            vin = self.vin.strip()
            if len(vin) != 17:
                from django.core.exceptions import ValidationError
                raise ValidationError({"vin": "VIN must be exactly 17 characters."})
            self.vin = vin.upper()