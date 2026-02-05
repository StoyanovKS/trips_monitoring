from django import forms

from logbook.models import Tag
from .models import Car


class TagsCheckboxMixin:
    def setup_tags(self):
        if "tags" in self.fields:
            self.fields["tags"].required = False
            self.fields["tags"].widget = forms.CheckboxSelectMultiple()
            self.fields["tags"].queryset = Tag.objects.order_by("name")
            self.fields["tags"].help_text = "Select one or more tags."
            self.fields["tags"].empty_label = None


class CarCreateForm(TagsCheckboxMixin, forms.ModelForm):
    class Meta:
        model = Car
        exclude = ("owner", "created_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["brand"].label = "Brand"
        self.fields["brand"].widget.attrs.update({"placeholder": "e.g. VW"})

        self.fields["model"].label = "Model"
        self.fields["model"].widget.attrs.update({"placeholder": "e.g. Golf"})

        self.fields["year"].label = "Year"
        self.fields["year"].widget.attrs.update({"placeholder": "2011"})

        self.fields["fuel"].label = "Fuel"
        self.fields["gearbox"].label = "Gearbox type"

        self.fields["vin"].label = "VIN (optional)"
        self.fields["vin"].widget.attrs.update({"placeholder": "17 characters"})

        self.fields["photo"].label = "Picture (optional)"
        self.fields["tags"].label = "Tags"

        self.setup_tags()


class CarEditForm(CarCreateForm):
    pass
