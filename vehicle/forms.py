from django import forms
from .models import Vehicle


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_number', 'vehicle_type', 'vehicle_model', 'vehicle_description']
