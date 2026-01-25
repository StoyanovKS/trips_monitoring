from django.urls import path
from .views import CarStatsAPIView, CarTripsAPIView

urlpatterns = [
    path("cars/<int:car_id>/stats/", CarStatsAPIView.as_view(), name="api-car-stats"),
    path("cars/<int:car_id>/trips/", CarTripsAPIView.as_view(), name="api-car-trips"),
]