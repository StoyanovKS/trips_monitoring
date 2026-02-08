from django.urls import path
from .views import (
    TripListView, TripDetailView, TripCreateView, TripUpdateView, TripDeleteView,
    RefuelListView, RefuelDetailView, RefuelCreateView, RefuelUpdateView, RefuelDeleteView
)

urlpatterns = [
    # Trips related urls
    path("trips/", TripListView.as_view(), name="trip-list"),
    path("trips/create/", TripCreateView.as_view(), name="trip-create"),
    path("trips/<int:pk>/", TripDetailView.as_view(), name="trip-detail"),
    path("trips/<int:pk>/edit/", TripUpdateView.as_view(), name="trip-edit"),
    path("trips/<int:pk>/delete/", TripDeleteView.as_view(), name="trip-delete"),

    # Refueling related urls
    path("refuels/", RefuelListView.as_view(), name="refuel-list"),
    path("refuels/create/", RefuelCreateView.as_view(), name="refuel-create"),
    path("refuels/<int:pk>/", RefuelDetailView.as_view(), name="refuel-detail"),
    path("refuels/<int:pk>/edit/", RefuelUpdateView.as_view(), name="refuel-edit"),
    path("refuels/<int:pk>/delete/", RefuelDeleteView.as_view(), name="refuel-delete"),
]
