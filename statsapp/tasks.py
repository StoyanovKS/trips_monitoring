from celery import shared_task
from decimal import Decimal
from django.db.models import Sum, F
from django.db.models.functions import Coalesce
from django.utils import timezone

from garage.models import Car
from logbook.models import Trip, Refuel
from .models import MonthlyCarStat


@shared_task
def recalculate_monthly_stats(car_id: int, year: int, month: int) -> int:
    """
    Recalculates MonthlyCarStat for a given car + year/month.
    Returns the MonthlyCarStat id.
    """
    car = Car.objects.filter(pk=car_id).first()
    if not car:
        return 0
    start = timezone.datetime(year=year, month=month, day=1).date()
    if month == 12:
        end = timezone.datetime(year=year + 1, month=1, day=1).date()
    else:
        end = timezone.datetime(year=year, month=month + 1, day=1).date()

    trips_qs = Trip.objects.filter(car_id=car_id, start_date__gte=start, start_date__lt=end)
    refuels_qs = Refuel.objects.filter(car_id=car_id, date__gte=start, date__lt=end)

    trips_count = trips_qs.count()
    total_distance_km = trips_qs.aggregate(
        total=Coalesce(Sum(F("end_odometer") - F("start_odometer")), 0)
    )["total"] or 0

    refuels_count = refuels_qs.count()
    refuels_agg = refuels_qs.aggregate(
        liters=Coalesce(Sum("liters"), Decimal("0.00")),
        cost=Coalesce(Sum("total_cost"), Decimal("0.00")),
    )
    total_liters = refuels_agg["liters"] or Decimal("0.00")
    total_cost = refuels_agg["cost"] or Decimal("0.00")

    obj, _ = MonthlyCarStat.objects.update_or_create(
        car_id=car_id,
        year=year,
        month=month,
        defaults={
            "trips_count": trips_count,
            "total_distance_km": int(total_distance_km),
            "refuels_count": refuels_count,
            "total_fuel_liters": total_liters,
            "total_fuel_cost": total_cost,
        },
    )
    return obj.id


@shared_task
def recalculate_all_cars_current_month() -> int:
    today = timezone.localdate()
    year, month = today.year, today.month

    car_ids = list(Car.objects.values_list("id", flat=True))
    for car_id in car_ids:
        recalculate_monthly_stats.delay(car_id, year, month)

    return len(car_ids)