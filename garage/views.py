from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.mixins import OwnerQuerySetMixin
from .models import Car
from .forms import CarCreateForm, CarEditForm


class CarListView(OwnerQuerySetMixin, ListView):
    model = Car
    template_name = "garage/car_list.html"
    context_object_name = "cars"


class CarDetailView(OwnerQuerySetMixin, DetailView):
    model = Car
    template_name = "garage/car_detail.html"
    context_object_name = "car"


class CarCreateView(OwnerQuerySetMixin, CreateView):
    model = Car
    form_class = CarCreateForm
    template_name = "garage/car_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("car-detail", kwargs={"pk": self.object.pk})


class CarUpdateView(OwnerQuerySetMixin, UpdateView):
    model = Car
    form_class = CarEditForm
    template_name = "garage/car_form.html"

    def get_success_url(self):
        return reverse_lazy("car-detail", kwargs={"pk": self.object.pk})


class CarDeleteView(OwnerQuerySetMixin, DeleteView):
    model = Car
    template_name = "garage/car_confirm_delete.html"
    success_url = reverse_lazy("car-list")