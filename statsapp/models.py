from django.db import models


class MonthlyCarStat(models.Model):
    car = models.ForeignKey("garage.Car", on_delete=models.CASCADE, related_name="monthly_stats")
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()  # 1..12

    trips_count = models.PositiveIntegerField(default=0)
    total_distance_km = models.PositiveIntegerField(default=0)

    refuels_count = models.PositiveIntegerField(default=0)
    total_fuel_liters = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_fuel_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("car", "year", "month")
        ordering = ("-year", "-month")

    def __str__(self):
        return f"{self.car} | {self.year}-{self.month:02d}"