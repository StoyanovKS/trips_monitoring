from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, F
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.views.generic import TemplateView

from garage.models import Car
from logbook.models import Trip, Refuel


class MonthlyReportView(LoginRequiredMixin, TemplateView):
    template_name = "statsapp/monthly_report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.localdate()
        year = int(self.request.GET.get("year", today.year))
        month = int(self.request.GET.get("month", today.month))

        cars = Car.objects.filter(owner=self.request.user).order_by("brand", "model", "year")

        car_id = self.request.GET.get("car")
        selected_car = None
        if car_id:
            try:
                car_id_int = int(car_id)
                selected_car = cars.filter(id=car_id_int).first()
            except ValueError:
                selected_car = None

        
        trips_qs = Trip.objects.filter(
            car__owner=self.request.user,
            start_date__year=year,
            start_date__month=month,
        )

        refuels_qs = Refuel.objects.filter(
            car__owner=self.request.user,
            date__year=year,
            date__month=month,
        )

        if selected_car:
            trips_qs = trips_qs.filter(car=selected_car)
            refuels_qs = refuels_qs.filter(car=selected_car)

        
        trips_by_car = (
            trips_qs.values("car_id", "car__brand", "car__model", "car__year")
            .annotate(
                trips_count=Count("id"),
                total_distance_km=Coalesce(Sum(F("end_odometer") - F("start_odometer")), 0),
            )
        )

        
        refuels_by_car_currency = (
            refuels_qs.values("car_id", "currency")
            .annotate(
                refuels_count=Count("id"),
                total_fuel_liters=Coalesce(Sum("liters"), Decimal("0")),
                total_fuel_cost=Coalesce(Sum("total_cost"), Decimal("0")),
            )
            .order_by("car_id", "currency")
        )

      
        refuels_map = {(r["car_id"], r["currency"]): r for r in refuels_by_car_currency}

        FX_EUR_BGN = Decimal("1.95583")

        
        stats = []
        for t in trips_by_car:
            car_id_val = t["car_id"]
            car_label = f'{t["car__brand"]} {t["car__model"]} ({t["car__year"]})'

            currencies_for_car = sorted({c for (cid, c) in refuels_map.keys() if cid == car_id_val})
            if not currencies_for_car:
                currencies_for_car = ["-"]

            for currency in currencies_for_car:
                r = refuels_map.get((car_id_val, currency), {})
                stats.append({
                    "car_id": car_id_val,
                    "car_label": car_label,
                    "currency": currency,
                    "trips_count": t["trips_count"],
                    "total_distance_km": t["total_distance_km"],
                    "refuels_count": r.get("refuels_count", 0),
                    "total_fuel_liters": r.get("total_fuel_liters", Decimal("0")),
                    "total_fuel_cost": r.get("total_fuel_cost", Decimal("0")),
                })

        
        
        trip_car_ids = {t["car_id"] for t in trips_by_car}
        for r in refuels_by_car_currency:
            if r["car_id"] not in trip_car_ids:
                car_obj = cars.filter(id=r["car_id"]).first()
                if car_obj:
                    stats.append({
                        "car_id": r["car_id"],
                        "car_label": f"{car_obj.brand} {car_obj.model} ({car_obj.year})",
                        "currency": r["currency"],
                        "trips_count": 0,
                        "total_distance_km": 0,
                        "refuels_count": r["refuels_count"],
                        "total_fuel_liters": r["total_fuel_liters"],
                        "total_fuel_cost": r["total_fuel_cost"],
                    })

        
        trips_totals = trips_qs.aggregate(
            trips_count=Count("id"),
            total_distance_km=Coalesce(Sum(F("end_odometer") - F("start_odometer")), 0),
        )
        refuels_totals = refuels_qs.aggregate(
            refuels_count=Count("id"),
            total_fuel_liters=Coalesce(Sum("liters"), Decimal("0")),
        )

     
        total_cost_eur = Decimal("0")
        for r in refuels_by_car_currency:
            cost = Decimal(r["total_fuel_cost"] or 0)
            if r["currency"] == "BGN":
                total_cost_eur += cost / FX_EUR_BGN
            elif r["currency"] == "EUR":
                total_cost_eur += cost
            else:
                total_cost_eur += cost

        totals = {
            "trips_count": trips_totals["trips_count"] or 0,
            "total_distance_km": int(trips_totals["total_distance_km"] or 0),
            "refuels_count": refuels_totals["refuels_count"] or 0,
            "total_fuel_liters": refuels_totals["total_fuel_liters"] or Decimal("0"),
            "total_fuel_cost_eur": total_cost_eur,
            "fx_eur_bgn": FX_EUR_BGN,
        }

        context.update({
            "cars": cars,
            "selected_car": selected_car,
            "year": year,
            "month": month,
            "stats": stats,
            "totals": totals,
        })
        return context
