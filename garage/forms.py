from django import forms
from .models import Car


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        # owner се задава в view-а, не в формата
        exclude = ("owner", "created_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["brand"].label = "Марка"
        self.fields["model"].label = "Модел"
        self.fields["year"].label = "Година"
        self.fields["fuel"].label = "Гориво"
        self.fields["gearbox"].label = "Скоростна кутия"
        self.fields["vin"].label = "VIN (по желание)"
        self.fields["photo"].label = "Снимка (по желание)"
        self.fields["tags"].label = "Тагове"

        self.fields["brand"].widget.attrs.update({"placeholder": "напр. Honda"})
        self.fields["model"].widget.attrs.update({"placeholder": "напр. Accord"})
        self.fields["year"].widget.attrs.update({"placeholder": "2011"})
        self.fields["vin"].widget.attrs.update({"placeholder": "17 символа (ако имаш)"})

        # friendly help
        self.fields["tags"].help_text = "Избери тагове (по желание)."


class CarEditForm(CarCreateForm):
    """
    Същото като create, но показваме owner като disabled поле (изискване #2).
    """
    owner = forms.CharField(label="Собственик", required=False, disabled=True)

    class Meta(CarCreateForm.Meta):
        exclude = ("created_at",)  # няма owner тук, понеже го добавяме като disabled поле

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # disabled owner (display only)
        if self.instance and self.instance.pk:
            self.fields["owner"].initial = getattr(self.instance.owner, "username", str(self.instance.owner))
