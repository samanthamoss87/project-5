from django import forms
from booking.models import Treatments

class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatments
        fields = ['title', 'description', 'half_hour', 'one_hour', 'two_hour']
        labels = {
            'half_hour': 'Price for 30 mins',
            'one_hour': 'Price for 1 hour',
            'two_hour': 'Price for 2 hours',
        }
        widgets = {
            'half_hour': forms.NumberInput(attrs={'min': '1', 'step': '0.01'}),
            'one_hour': forms.NumberInput(attrs={'min': '1', 'step': '0.01'}),
            'two_hour': forms.NumberInput(attrs={'min': '1', 'step': '0.01'}),
        }

    def clean_half_hour(self):
        value = self.cleaned_data['half_hour']
        if value < 1:
            raise forms.ValidationError("Price must be at least £1.00")
        return value

    def clean_one_hour(self):
        value = self.cleaned_data['one_hour']
        if value < 1:
            raise forms.ValidationError("Price must be at least £1.00")
        return value

    def clean_two_hour(self):
        value = self.cleaned_data['two_hour']
        if value < 1:
            raise forms.ValidationError("Price must be at least £1.00")
        return value