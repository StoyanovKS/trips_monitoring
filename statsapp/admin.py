from django.contrib import admin
from .models import MonthlyCarStat


@admin.register(MonthlyCarStat)
class MonthlyCarStatAdmin(admin.ModelAdmin):
    list_display = ("car", "year", "month", "trips_count", "total_distance_km", "refuels_count", "total_fuel_cost", "updated_at")
    list_filter = ("year", "month")
    search_fields = ("car__brand", "car__model", "car__owner__username")