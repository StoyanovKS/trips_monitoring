from decimal import Decimal

from django.db.models import Sum, F
from django.db.models.functions import Coalesce
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from garage.models import Car
from logbook.models import Trip, Refuel
from .serializers import CarStatsSerializer, TripSerializer
from .permissions import IsOwnerOrManager


class CarStatsAPIView(APIView):
    permission_classes = [IsOwnerOrManager]

    def get(self, request, car_id: int):
        car = Car.objects.filter(pk=car_id).first()
        if not car:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)


        self.check_object_permissions(request, car)
        trips_qs = Trip.objects.filter(car_id=car_id)
        refuels_qs = Refuel.objects.filter(car_id=car_id)
        trips_count = trips_qs.count()
        total_distance_km = trips_qs.aggregate(
            total=Coalesce(Sum(F("end_odometer") - F("start_odometer")), 0)
        )["total"] or 0

        refuels_agg = refuels_qs.aggregate(
            liters=Coalesce(Sum("liters"), Decimal("0.00")),
            cost=Coalesce(Sum("total_cost"), Decimal("0.00")),
        )
        total_liters = refuels_agg["liters"] or Decimal("0.00")
        total_cost = refuels_agg["cost"] or Decimal("0.00")

        avg_cost_per_liter = Decimal("0.000")
        if total_liters > 0:
            avg_cost_per_liter = (total_cost / total_liters).quantize(Decimal("0.001"))

        data = {
            "car_id": car.id,
            "car_name": str(car),
            "trips_count": trips_count,
            "total_distance_km": int(total_distance_km),
            "refuels_count": refuels_qs.count(),
            "total_fuel_liters": total_liters,
            "total_fuel_cost": total_cost,
            "avg_cost_per_liter": avg_cost_per_liter,
        }

        serializer = CarStatsSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CarTripsAPIView(APIView):
    permission_classes = [IsOwnerOrManager]

    def get(self, request, car_id: int):
        car = Car.objects.filter(pk=car_id).first()
        if not car:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, car)

        trips = (
            Trip.objects.filter(car_id=car_id)
            .select_related("car")
            .order_by("-start_date", "-created_at")
        )

        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)