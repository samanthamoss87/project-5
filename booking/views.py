from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from .forms import BookingForm, ContactForm
from .models import Treatments, Booking


def home(request):
    return render(request, 'home.html')


def treatments(request):
    treatment_list = Treatments.objects.all()
    return render(request, 'treatments.html', {'treatments': treatment_list})


@login_required
def book_now(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.duration = int(form.cleaned_data['duration'])
            booking.save()
            return redirect('booking_success')

        else:
            render(request, 'booking.html', {'form': form})
    else:
        form = BookingForm()
    
    return render(request, 'booking.html', {'form': form})


def booking_success(request):
    return render(request, 'booking_success.html')


def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.user == request.user:
        booking.delete()
        from django.contrib import messages
        messages.success(request, 'Your booking has been canceled successfully.')
    else:
        messages.error(request, 'You do not have permission to cancel this booking.')
    return redirect('dashboard')



def contact(request):
    success = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form, 'success': success})

def coming_soon(request):
    return render(request, 'coming_soon.html')


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)