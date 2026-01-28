from django.contrib import admin
from .models import Trip, Refuel, Expense, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("car", "from_city", "to_city", "start_date", "end_date", "created_by")
    search_fields = ("from_city", "to_city", "car__brand", "car__model", "created_by__username")
    list_filter = ("start_date", "end_date")
    autocomplete_fields = ("car", "created_by")
    filter_horizontal = ("tags",)


@admin.register(Refuel)
class RefuelAdmin(admin.ModelAdmin):
    list_display = ("car", "date", "odometer", "liters", "total_cost", "created_by")
    list_filter = ("date",)
    search_fields = ("car__brand", "car__model", "station", "created_by__username")
    autocomplete_fields = ("car", "created_by")


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("expense_type", "amount", "trip", "created_at")
    list_filter = ("expense_type", "created_at")
    search_fields = ("note",)
    autocomplete_fields = ("trip",)
