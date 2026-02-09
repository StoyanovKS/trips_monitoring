from django import forms
from django.core.exceptions import ValidationError
from garage.models import Car
from .models import Trip, Refuel, Expense, Tag


class TagsCheckboxMixin:
    def setup_tags(self):
        if "tags" in self.fields:
            self.fields["tags"].required = False
            self.fields["tags"].widget = forms.CheckboxSelectMultiple()
            self.fields["tags"].queryset = Tag.objects.all().order_by("name")
            self.fields["tags"].help_text = "Select one or more tags."


class TripCreateForm(TagsCheckboxMixin, forms.ModelForm):
    class Meta:
        model = Trip
        exclude = ("created_by", "created_at")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if self.user is not None and "car" in self.fields:
            self.fields["car"].queryset = (
                Car.objects.filter(owner=self.user)
                .order_by("brand", "model", "year")
            )
        if "car" in self.fields:
            self.fields["car"].label = "Car"
        if "start_odometer" in self.fields:
            self.fields["start_odometer"].label = "KM (start)"
        if "end_odometer" in self.fields:
            self.fields["end_odometer"].label = "KM (end)"
        if "start_date" in self.fields:
            self.fields["start_date"].label = "Date (start)"
        if "end_date" in self.fields:
            self.fields["end_date"].label = "Date (end)"
        if "from_city" in self.fields:
            self.fields["from_city"].label = "From"
        if "to_city" in self.fields:
            self.fields["to_city"].label = "To"
        if "notes" in self.fields:
            self.fields["notes"].label = "Notes"
        if "tags" in self.fields:
            self.fields["tags"].label = "Tags"        
        if "from_city" in self.fields:
            self.fields["from_city"].widget.attrs.update({"placeholder": "e.g. Sofia"})
        if "to_city" in self.fields:
            self.fields["to_city"].widget.attrs.update({"placeholder": "e.g. Plovdiv"})
        if "notes" in self.fields:
            self.fields["notes"].widget.attrs.update({"placeholder": "Optional"})

        
        self.setup_tags()

    def clean(self):
        cleaned = super().clean()
        start_odo = cleaned.get("start_odometer")
        end_odo = cleaned.get("end_odometer")
        start_date = cleaned.get("start_date")
        end_date = cleaned.get("end_date")
        if start_odo is not None and end_odo is not None and end_odo < start_odo:
            self.add_error("end_odometer", "The final odometer must be higher than the initial one.")
        if start_date and end_date and end_date < start_date:
            self.add_error("end_date", "The end date must be after the start date.")
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

        # Default currency follows the user's preference when creating a new refuel.
        if self.user is not None and not self.instance.pk and "currency" in self.fields:
            self.fields["currency"].initial = getattr(self.user, "preferred_currency", Refuel.CurrencyChoices.BGN)

        
        if self.user is not None and "car" in self.fields:
            self.fields["car"].queryset = (
                Car.objects.filter(owner=self.user)
                .order_by("brand", "model", "year")
            )
        if "car" in self.fields:
            self.fields["car"].label = "Car"
        if "date" in self.fields:
            self.fields["date"].label = "Date"
        if "odometer" in self.fields:
            self.fields["odometer"].label = "Odometer"
        if "liters" in self.fields:
            self.fields["liters"].label = "Liters"
        if "total_cost" in self.fields:
            self.fields["total_cost"].label = "Total cost"
        if "currency" in self.fields:
            self.fields["currency"].label = "Currency"
        if "fuel_type" in self.fields:
            self.fields["fuel_type"].label = "Fuel type (optional)"
        if "station" in self.fields:
            self.fields["station"].label = "Station (optional)"
        if "liters" in self.fields:
            self.fields["liters"].widget.attrs.update({"placeholder": "42.5"})
        if "total_cost" in self.fields:
            self.fields["total_cost"].widget.attrs.update({"placeholder": "120.00"})
        if "station" in self.fields:
            self.fields["station"].widget.attrs.update({"placeholder": "Shell"})

    def clean(self):
        cleaned = super().clean()
        liters = cleaned.get("liters")
        total_cost = cleaned.get("total_cost")
        odometer = cleaned.get("odometer")
        car = cleaned.get("car")
        date = cleaned.get("date")

        if liters is not None and liters <= 0:
            self.add_error("liters", "Liters must be a positive number.")

        if total_cost is not None and total_cost <= 0:
            self.add_error("total_cost", "Total cost must be a positive number.")

        # Odometer consistency should be checked against refuels around the selected DATE,
        # not against the latest refuel overall.
        if car and odometer is not None and date:
            base_qs = Refuel.objects.filter(car=car).exclude(pk=self.instance.pk)

            prev_refuel = (
                base_qs.filter(date__lt=date)
                .order_by("-date", "-created_at")
                .first()
            )
            next_refuel = (
                base_qs.filter(date__gt=date)
                .order_by("date", "created_at")
                .first()
            )

            if prev_refuel and odometer < prev_refuel.odometer:
                self.add_error(
                    "odometer",
                    f"Odometer must be at least {prev_refuel.odometer} (previous refuel before this date).",
                )

            # Optional: keep monotonicity if user inserts an older refuel.
            if next_refuel and odometer > next_refuel.odometer:
                self.add_error(
                    "odometer",
                    f"Odometer must be at most {next_refuel.odometer} (next refuel after this date).",
                )

        return cleaned


class RefuelEditForm(RefuelCreateForm):
    class Meta:
        model = Refuel
        fields = ("car", "date", "odometer", "liters", "total_cost", "currency", "fuel_type", "station")


class ExpenseCreateForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ("trip", "expense_type", "amount", "note")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user is not None and "trip" in self.fields:
            self.fields["trip"].queryset = (
                Trip.objects.filter(car__owner=self.user)
                .order_by("-start_date", "-created_at")
            )

        if "trip" in self.fields:
            self.fields["trip"].label = "Trip"
        if "expense_type" in self.fields:
            self.fields["expense_type"].label = "Expense type"
        if "amount" in self.fields:
            self.fields["amount"].label = "Amount"
        if "note" in self.fields:
            self.fields["note"].label = "Note"
            self.fields["note"].widget.attrs.update({"placeholder": "e.g. vignette, parking, etc."})

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount is not None and amount <= 0:
            raise ValidationError("Amount must be positive.")
        return amount


class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].label = "Tag"
        self.fields["name"].widget.attrs.update({"placeholder": "Highway"})
        self.fields["name"].help_text = "Up to 30 characters. Must be unique."
        self.fields["name"].error_messages = {"unique": "This tag already exists."}

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        if len(name) < 2:
            raise ValidationError("Tag must be at least 2 characters.")
        return name
