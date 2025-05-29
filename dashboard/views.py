from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from booking.models import Booking
from booking.forms import BookingForm

@login_required
def dashboard(request):

    today = datetime.today().date()

    future_bookings = Booking.objects.filter(user=request.user, date__gte=today).order_by('date', 'start_time')
    past_bookings = Booking.objects.filter(user=request.user, date__lt=today).order_by('-date', '-start_time')

    context = {
        'future_bookings': future_bookings,
        'past_bookings': past_bookings,
    }

    return render(request, 'dashboard/dashboard.html', context)
