from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
from booking.models import Booking, Treatments 
from booking.forms import BookingForm
from .forms import TreatmentForm


def is_superuser(user):
    return user.is_superuser

@login_required
def dashboard(request):
    today = datetime.today().date()


    future_bookings = Booking.objects.filter(user=request.user, date__gte=today).order_by('date', 'start_time')
    past_bookings = Booking.objects.filter(user=request.user, date__lt=today).order_by('-date', '-start_time')


    treatments = Treatments.objects.all() if request.user.is_superuser else []

    context = {
        'future_bookings': future_bookings,
        'past_bookings': past_bookings,
        'treatments': treatments,
    }

    return render(request, 'dashboard/dashboard.html', context)


@user_passes_test(is_superuser)
def add_treatment(request):
    if request.method == 'POST':
        form = TreatmentForm(request.POST)
        if form.is_valid():
            form.save()
            print("Form is valid. Treatment saved.")
            return redirect('dashboard:dashboard')
        else:
            print("Form errors:", form.errors)
    else:
        form = TreatmentForm()

    return render(request, 'dashboard/treatment_form.html', {'form': form})



@user_passes_test(is_superuser)
def edit_treatment(request, pk):
    treatment = get_object_or_404(Treatments, pk=pk)
    
    if request.method == 'POST':
        form = TreatmentForm(request.POST, instance=treatment)
        if form.is_valid():
            form.save()
            return redirect('dashboard:dashboard')
        else:
            print("Form errors:", form.errors)
    else:
        form = TreatmentForm(instance=treatment)
    
    return render(request, 'dashboard/treatment_form.html', {'form': form})


@user_passes_test(is_superuser)
def delete_treatment(request, pk):
    treatment = get_object_or_404(Treatments, pk=pk)
    
    if request.method == 'POST':
        treatment.delete()
        return redirect('dashboard:dashboard')
    
    return render(request, 'dashboard/treatment_confirm_delete.html', {'treatment': treatment})