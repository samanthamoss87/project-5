from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid
import datetime
from .models import  Booking, Contact


class BookingForm(forms.ModelForm):
    DURATION_CHOICES = [
        (30, '30 Minutes - $55'),
        (60, '60 Minutes - $80'),
        (120, '120 Minutes - $110'),
    ]

    duration = forms.ChoiceField(choices=DURATION_CHOICES, widget=forms.RadioSelect)
    start_time = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Booking
        fields = ['treatment', 'date', 'start_time', 'duration']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'treatment': forms.Select(attrs={"class": 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].choices = self.generate_time_slots()

    def generate_time_slots(self):
        time_slots = []
        start_time = datetime.time(9, 0)
        end_time = datetime.time(22, 0)
        delta = datetime.timedelta(minutes=30)

        current_time = datetime.datetime.combine(datetime.date.today(), start_time)
        end_datetime = datetime.datetime.combine(datetime.date.today(), end_time)

        while current_time <= end_datetime:
            time_slots.append((current_time.time().strftime('%H:%M'), current_time.strftime('%I:%M %p')))
            current_time += delta

        return time_slots

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        duration = int(cleaned_data.get('duration', 0))

        if date and start_time and duration:
            start_time = datetime.datetime.strptime(start_time, '%H:%M').time()
            start_dt = datetime.datetime.combine(date, start_time)
            end_dt = start_dt + datetime.timedelta(minutes=duration)
            now = datetime.datetime.now()

            if start_dt < now:
                raise ValidationError("You cannot book an appointment in the past.")

            conflicts = Booking.objects.filter(
                date=date,
                start_time__lt=end_dt.time(),
                end_time__gt=start_dt.time()
            )
            if conflicts.exists():
                raise ValidationError("This time slot is already booked")

        return cleaned_data


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']