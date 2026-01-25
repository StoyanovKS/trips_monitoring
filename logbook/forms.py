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
        self.fields["start_odometer"].label = "Километраж (старт)"
        self.fields["end_odometer"].label = "Километраж (край)"
        self.fields["start_date"].label = "Дата (старт)"
        self.fields["end_date"].label = "Дата (край)"
        self.fields["from_city"].label = "От"
        self.fields["to_city"].label = "До"
        self.fields["notes"].label = "Бележки"
        self.fields["tags"].label = "Тагове"

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

        # end>=start
        if start_odo is not None and end_odo is not None and end_odo < start_odo:
            self.add_error("end_odometer", "Крайният километраж не може да е по-малък от началния.")

        # date ranges
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
        self.user = kwargs.pop("user", None)  # optionally pass user for checks later
        super().__init__(*args, **kwargs)

        self.fields["car"].label = "Автомобил"
        self.fields["date"].label = "Дата"
        self.fields["odometer"].label = "Километраж"
        self.fields["liters"].label = "Литри"
        self.fields["total_cost"].label = "Обща сума"
        self.fields["fuel_type"].label = "Тип гориво (по желание)"
        self.fields["station"].label = "Бензиностанция (по желание)"

        self.fields["liters"].widget.attrs.update({"placeholder": "напр. 42.5"})
        self.fields["total_cost"].widget.attrs.update({"placeholder": "напр. 120.00"})
        self.fields["station"].widget.attrs.update({"placeholder": "напр. Shell"})

    def clean(self):
        cleaned = super().clean()

        liters = cleaned.get("liters")
        total_cost = cleaned.get("total_cost")
        odometer = cleaned.get("odometer")
        car = cleaned.get("car")

        if liters is not None and liters <= 0:
            self.add_error("liters", "Литрите трябва да са положително число.")

        if total_cost is not None and total_cost <= 0:
            self.add_error("total_cost", "Сумата трябва да е положително число.")

        # Odometer monotonic: odometer must be >= last refuel odometer for same car
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
                    f"Километражът трябва да е поне {last.odometer} (последното зареждане)."
                )

        return cleaned


class ExpenseCreateForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ("trip", "expense_type", "amount", "note")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["trip"].label = "Пътуване (по желание)"
        self.fields["expense_type"].label = "Тип разход"
        self.fields["amount"].label = "Сума"
        self.fields["note"].label = "Бележка"

        self.fields["note"].widget.attrs.update({"placeholder": "напр. винетка, паркинг..."})

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount is not None and amount <= 0:
            raise ValidationError("Сумата трябва да е положително число.")
        return amount


class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("name",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].label = "Таг"
        self.fields["name"].widget.attrs.update({"placeholder": "напр. highway"})
        self.fields["name"].help_text = "До 30 символа. Уникално име."
        self.fields["name"].error_messages = {
            "unique": "Този таг вече съществува."
        }

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        if len(name) < 2:
            raise ValidationError("Тагът трябва да е поне 2 символа.")
        return name
