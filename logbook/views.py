from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from garage.models import Car
from .models import Trip, Refuel
from .forms import TripCreateForm, TripEditForm, RefuelCreateForm


# -------------------------
# Trips
# -------------------------

class TripListView(ListView):
    model = Trip
    template_name = "logbook/trip_list.html"
    context_object_name = "trips"

    def get_queryset(self):
        return (
            Trip.objects.select_related("car")
            .filter(car__owner=self.request.user)
            .order_by("-start_date", "-created_at")
        )


class TripDetailView(DetailView):
    model = Trip
    template_name = "logbook/trip_detail.html"
    context_object_name = "trip"

    def get_queryset(self):
        return Trip.objects.select_related("car").filter(car__owner=self.request.user)


class TripCreateView(CreateView):
    model = Trip
    form_class = TripCreateForm
    template_name = "logbook/trip_form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # show only user's cars
        form.fields["car"].queryset = Car.objects.filter(owner=self.request.user).order_by("brand", "model", "year")
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("trip-detail", kwargs={"pk": self.object.pk})


class TripUpdateView(UpdateView):
    model = Trip
    form_class = TripEditForm
    template_name = "logbook/trip_form.html"

    def get_queryset(self):
        return Trip.objects.filter(car__owner=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["car"].queryset = Car.objects.filter(owner=self.request.user).order_by("brand", "model", "year")
        return form

    def get_success_url(self):
        return reverse_lazy("trip-detail", kwargs={"pk": self.object.pk})


class TripDeleteView(DeleteView):
    model = Trip
    template_name = "logbook/trip_confirm_delete.html"
    success_url = reverse_lazy("trip-list")

    def get_queryset(self):
        return Trip.objects.filter(car__owner=self.request.user)


# -------------------------
# Refuels
# -------------------------

class RefuelListView(ListView):
    model = Refuel
    template_name = "logbook/refuel_list.html"
    context_object_name = "refuels"

    def get_queryset(self):
        return (
            Refuel.objects.select_related("car")
            .filter(car__owner=self.request.user)
            .order_by("-date", "-created_at")
        )


class RefuelDetailView(DetailView):
    model = Refuel
    template_name = "logbook/refuel_detail.html"
    context_object_name = "refuel"

    def get_queryset(self):
        return Refuel.objects.select_related("car").filter(car__owner=self.request.user)


class RefuelCreateView(CreateView):
    model = Refuel
    form_class = RefuelCreateForm
    template_name = "logbook/refuel_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user  # if you want user-based validation later
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["car"].queryset = Car.objects.filter(owner=self.request.user).order_by("brand", "model", "year")
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("refuel-detail", kwargs={"pk": self.object.pk})


class RefuelUpdateView(UpdateView):
    model = Refuel
    form_class = RefuelCreateForm
    template_name = "logbook/refuel_form.html"

    def get_queryset(self):
        return Refuel.objects.filter(car__owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["car"].queryset = Car.objects.filter(owner=self.request.user).order_by("brand", "model", "year")
        return form

    def get_success_url(self):
        return reverse_lazy("refuel-detail", kwargs={"pk": self.object.pk})


class RefuelDeleteView(DeleteView):
    model = Refuel
    template_name = "logbook/refuel_confirm_delete.html"
    success_url = reverse_lazy("refuel-list")

    def get_queryset(self):
        return Refuel.objects.filter(car__owner=self.request.user)
