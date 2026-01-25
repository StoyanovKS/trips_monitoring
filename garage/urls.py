from django.urls import path
from .views import (
    CarListView, CarDetailView, CarCreateView, CarUpdateView, CarDeleteView
)

urlpatterns = [
    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/create/", CarCreateView.as_view(), name="car-create"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("cars/<int:pk>/edit/", CarUpdateView.as_view(), name="car-edit"),
    path("cars/<int:pk>/delete/", CarDeleteView.as_view(), name="car-delete"),
]