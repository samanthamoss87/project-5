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