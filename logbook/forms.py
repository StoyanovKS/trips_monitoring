from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Trip, Refuel, Expense, Tag


class TripCreateForm(forms.ModelForm):
    class Meta:
        model = Trip
        exclude = ("created_by", "created_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["car"].label = "Автомобил"
        self.fields["start_odometer"].label = "KM (start)"
        self.fields["end_odometer"].label = "KM (end)"
        self.fields["start_date"].label = "Date (start)"
        self.fields["end_date"].label = "Date (end)"
        self.fields["from_city"].label = "From"
        self.fields["to_city"].label = "To"
        self.fields["notes"].label = "notes"
        self.fields["tags"].label = "tags"

        self.fields["from_city"].widget.attrs.update({"placeholder": "напр. София"})
        self.fields["to_city"].widget.attrs.update({"placeholder": "напр. Плевен"})
        self.fields["notes"].widget.attrs.update({"placeholder": "по желание..."})

        self.error_messages = {
            "invalid": "Невалидни данни. Провери полетата.",
        }

    def clean(self):
        cleaned = super().clean()

        start_odo = cleaned.get("start_odometer")
        end_odo = cleaned.get("end_odometer")
        start_date = cleaned.get("start_date")
        end_date = cleaned.get("end_date")

        
        if start_odo is not None and end_odo is not None and end_odo < start_odo:
            self.add_error("end_odometer", "Крайният километраж не може да е по-малък от началния.")

        
        if start_date and end_date and end_date < start_date:
            self.add_error("end_date", "Крайната дата не може да е преди началната.")

        return cleaned


class TripEditForm(TripCreateForm):
    pass


class RefuelCreateForm(forms.ModelForm):
    class Meta:
        model = Refuel
        exclude = ("created_by", "created_at")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)  
        super().__init__(*args, **kwargs)

        self.fields["car"].label = "Car"
        self.fields["date"].label = "Date"
        self.fields["odometer"].label = "Odometer"
        self.fields["liters"].label = "Liters"
        self.fields["total_cost"].label = "Total"
        self.fields["fuel_type"].label = "Fuel type (not mandatory)"
        self.fields["station"].label = "Station (not mandatory)"

        self.fields["liters"].widget.attrs.update({"placeholder": "42.5"})
        self.fields["total_cost"].widget.attrs.update({"placeholder": "120.00"})
        self.fields["station"].widget.attrs.update({"placeholder": "Shell"})

    def clean(self):
        cleaned = super().clean()

        liters = cleaned.get("liters")
        total_cost = cleaned.get("total_cost")
        odometer = cleaned.get("odometer")
        car = cleaned.get("car")

        if liters is not None and liters <= 0:
            self.add_error("liters", "Liters shall be positive number.")

        if total_cost is not None and total_cost <= 0:
            self.add_error("total_cost", "The sum shall be a positive number")

        
        if car and odometer is not None:
            last = (
                Refuel.objects.filter(car=car)
                .exclude(pk=self.instance.pk)
                .order_by("-date", "-created_at")
                .first()
            )
            if last and odometer < last.odometer:
                self.add_error(
                    "odometer",
                    f"KM shall be at least {last.odometer} (the last refuel)."
                )

        return cleaned


class ExpenseCreateForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ("trip", "expense_type", "amount", "note")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["trip"].label = "Trip"
        self.fields["expense_type"].label = "Cost type"
        self.fields["amount"].label = "Amount Paid"
        self.fields["note"].label = "Note"

        self.fields["note"].widget.attrs.update({"placeholder": "vignette, parking or else."})

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount is not None and amount <= 0:
            raise ValidationError("The sum shall be positive.")
        return amount


class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].label = "Таг"
        self.fields["name"].widget.attrs.update({"placeholder": "Highway"})
        self.fields["name"].help_text = "up to 30 symbols. it shall be unique."
        self.fields["name"].error_messages = {
            "unique": "The tag does not exist."
        }

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        if len(name) < 2:
            raise ValidationError("Tag shall be at least two symbols")
        return name
    
class RefuelEditForm(forms.ModelForm):
    class Meta:
        model = Refuel
        fields = ("car", "date", "odometer", "liters", "total_cost", "fuel_type", "station")