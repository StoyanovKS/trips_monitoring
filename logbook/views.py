from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .models import Trip, Refuel
from .forms import (
    TripCreateForm, TripEditForm,
    RefuelCreateForm, RefuelEditForm,
)


class TripListView(LoginRequiredMixin, ListView):
    model = Trip
    template_name = "logbook/trip_list.html"
    context_object_name = "trips"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("car", "created_by")
            .prefetch_related("tags")
            .filter(car__owner=self.request.user)
        )


class TripDetailView(LoginRequiredMixin, DetailView):
    model = Trip
    template_name = "logbook/trip_detail.html"
    context_object_name = "trip"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("car", "created_by")
            .prefetch_related("tags")
            .filter(car__owner=self.request.user)
        )


class TripCreateView(LoginRequiredMixin, CreateView):
    model = Trip
    form_class = TripCreateForm
    template_name = "logbook/trip_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("trip-detail", kwargs={"pk": self.object.pk})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TripUpdateView(LoginRequiredMixin, UpdateView):
    model = Trip
    form_class = TripEditForm
    template_name = "logbook/trip_form.html"

    def get_queryset(self):
        return super().get_queryset().filter(car__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy("trip-detail", kwargs={"pk": self.object.pk})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class TripDeleteView(LoginRequiredMixin, DeleteView):
    model = Trip
    template_name = "logbook/trip_confirm_delete.html"
    success_url = reverse_lazy("trip-list")

    def get_queryset(self):
        return super().get_queryset().filter(car__owner=self.request.user)


class RefuelListView(LoginRequiredMixin, ListView):
    model = Refuel
    template_name = "logbook/refuel_list.html"
    context_object_name = "refuels"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("car", "created_by")
            .filter(car__owner=self.request.user)
        )


class RefuelDetailView(LoginRequiredMixin, DetailView):
    model = Refuel
    template_name = "logbook/refuel_detail.html"
    context_object_name = "refuel"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("car", "created_by")
            .filter(car__owner=self.request.user)
        )


class RefuelCreateView(LoginRequiredMixin, CreateView):
    model = Refuel
    form_class = RefuelCreateForm
    template_name = "logbook/refuel_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("refuel-detail", kwargs={"pk": self.object.pk})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class RefuelUpdateView(LoginRequiredMixin, UpdateView):
    model = Refuel
    form_class = RefuelEditForm
    template_name = "logbook/refuel_form.html"

    def get_queryset(self):
        return super().get_queryset().filter(car__owner=self.request.user)

    def get_success_url(self):
        return reverse_lazy("refuel-detail", kwargs={"pk": self.object.pk})
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class RefuelDeleteView(LoginRequiredMixin, DeleteView):
    model = Refuel
    template_name = "logbook/refuel_confirm_delete.html"
    success_url = reverse_lazy("refuel-list")

    def get_queryset(self):
        return super().get_queryset().filter(car__owner=self.request.user)
