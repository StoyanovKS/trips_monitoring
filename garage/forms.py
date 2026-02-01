from django import forms
from .models import Car


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        
        exclude = ("owner", "created_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["brand"].label = "Brand"
        self.fields["model"].label = "Model"
        self.fields["year"].label = "Year"
        self.fields["fuel"].label = "Fuel"
        self.fields["gearbox"].label = "Gearbox type"
        self.fields["vin"].label = "VIN (not mandatory)"
        self.fields["photo"].label = "Picture (not mandatory)"
        self.fields["tags"].label = "Tags"

        self.fields["brand"].widget.attrs.update({"placeholder": "ex. VW"})
        self.fields["model"].widget.attrs.update({"placeholder": "ex. Golf"})
        self.fields["year"].widget.attrs.update({"placeholder": "2011"})
        self.fields["vin"].widget.attrs.update({"placeholder": "17 symbols overall"})

        
        self.fields["tags"].help_text = "choose tags"


class CarEditForm(CarCreateForm):
  
    owner = forms.CharField(label="Owner", required=False, disabled=True)

    class Meta(CarCreateForm.Meta):
        exclude = ("created_at",)  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        if self.instance and self.instance.pk:
            self.fields["owner"].initial = getattr(self.instance.owner, "username", str(self.instance.owner))
