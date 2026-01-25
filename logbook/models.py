from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Trip(models.Model):
    car = models.ForeignKey(
        "garage.Car",
        on_delete=models.CASCADE,
        related_name="trips",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_trips",
    )

    start_odometer = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    end_odometer = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField(default=timezone.localdate)

    from_city = models.CharField(max_length=60)
    to_city = models.CharField(max_length=60)

    notes = models.TextField(blank=True)

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="trips",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-start_date", "-created_at")

    def __str__(self):
        return f"{self.car} | {self.from_city} -> {self.to_city} ({self.start_date})"

    @property
    def distance_km(self) -> int:
        """
        Derived distance from odometer values.
        """
        return max(0, self.end_odometer - self.start_odometer)

    def clean(self):
        super().clean()

        if self.end_odometer < self.start_odometer:
            raise ValidationError({"end_odometer": "End odometer cannot be smaller than start odometer."})

        if self.end_date < self.start_date:
            raise ValidationError({"end_date": "End date cannot be before start date."})


class Refuel(models.Model):
    car = models.ForeignKey(
        "garage.Car",
        on_delete=models.CASCADE,
        related_name="refuels",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_refuels",
    )

    date = models.DateField(default=timezone.localdate)
    odometer = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    liters = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Total cost in your currency.",
    )

    fuel_type = models.CharField(max_length=20, blank=True)
    station = models.CharField(max_length=60, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date", "-created_at")

    def __str__(self):
        return f"{self.car} | {self.date} | {self.liters}L"

    def clean(self):
        super().clean()
        # Example validation: keep it simple for now
        if self.station:
            self.station = self.station.strip()


class Expense(models.Model):
    class ExpenseType(models.TextChoices):
        TOLL = "toll", "Toll"
        PARKING = "parking", "Parking"
        SERVICE = "service", "Service"
        OTHER = "other", "Other"

    trip = models.ForeignKey(
        Trip,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses",
    )

    expense_type = models.CharField(
        max_length=20,
        choices=ExpenseType.choices,
        default=ExpenseType.OTHER,
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )

    note = models.CharField(max_length=120, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        if self.trip:
            return f"{self.expense_type} | {self.amount} | Trip #{self.trip_id}"
        return f"{self.expense_type} | {self.amount}"