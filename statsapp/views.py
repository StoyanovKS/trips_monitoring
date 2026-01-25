from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView

from garage.models import Car
from .models import MonthlyCarStat


class MonthlyReportView(LoginRequiredMixin, TemplateView):
    template_name = "statsapp/monthly_report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # current month by default
        today = timezone.localdate()
        year = int(self.request.GET.get("year", today.year))
        month = int(self.request.GET.get("month", today.month))

        cars = Car.objects.filter(owner=self.request.user).order_by("brand", "model", "year")

        # optional car filter (?car=ID)
        car_id = self.request.GET.get("car")
        stats_qs = MonthlyCarStat.objects.filter(
            car__owner=self.request.user,
            year=year,
            month=month,
        ).select_related("car")

        selected_car = None
        if car_id:
            try:
                car_id_int = int(car_id)
                selected_car = cars.filter(id=car_id_int).first()
                if selected_car:
                    stats_qs = stats_qs.filter(car_id=car_id_int)
            except ValueError:
                pass

        # totals for summary row
        totals = {
            "trips_count": 0,
            "total_distance_km": 0,
            "refuels_count": 0,
            "total_fuel_liters": 0,
            "total_fuel_cost": 0,
        }
        for s in stats_qs:
            totals["trips_count"] += s.trips_count
            totals["total_distance_km"] += s.total_distance_km
            totals["refuels_count"] += s.refuels_count
            totals["total_fuel_liters"] += float(s.total_fuel_liters)
            totals["total_fuel_cost"] += float(s.total_fuel_cost)

        context.update({
            "cars": cars,
            "selected_car": selected_car,
            "year": year,
            "month": month,
            "stats": stats_qs,
            "totals": totals,
        })
        return context