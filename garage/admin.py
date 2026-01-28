from django.contrib import admin
from .models import Car


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "year", "fuel", "gearbox", "owner")
    search_fields = ("brand", "model", "owner__username")
    list_filter = ("year", "fuel", "gearbox")
    autocomplete_fields = ("owner",)
