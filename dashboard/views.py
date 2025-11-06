from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime, timedelta
from booking.models import Booking, Treatments 
from booking.forms import BookingForm
from .forms import TreatmentForm
from newsletter.models import Subscribe


def is_superuser(user):
    return user.is_superuser

@login_required
def dashboard(request):
    from django.utils import timezone
    now = timezone.now()
    
    all_confirmed_bookings = Booking.objects.filter(user=request.user, status='confirmed')
    
    future_bookings = []
    past_bookings = []
    
    for booking in all_confirmed_bookings:
        booking_datetime = timezone.make_aware(datetime.combine(booking.date, booking.start_time))
        if booking_datetime > now:
            future_bookings.append(booking)
        else:
            past_bookings.append(booking)
    
    future_bookings.sort(key=lambda x: (x.date, x.start_time))
    past_bookings.sort(key=lambda x: (x.date, x.start_time), reverse=True)
    
    cancelled_bookings = Booking.objects.filter(user=request.user, status='cancelled').order_by('-date', '-start_time')

    treatments = Treatments.objects.all() if request.user.is_superuser else None

    context = {
        'future_bookings': future_bookings,
        'past_bookings': past_bookings,
        'cancelled_bookings': cancelled_bookings,
        'treatments': treatments,
        'user': request.user,
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


@user_passes_test(is_superuser)
def send_newsletter(request, pk):
    treatment = get_object_or_404(Treatments, pk=pk)
    
    if request.method == 'POST':
        description = request.POST.get('description', '')
        
        subscribers = Subscribe.objects.filter(is_active=True)
        if not subscribers.exists():
            messages.warning(request, 'No active subscribers found.')
            return redirect('dashboard:dashboard')
        
        recipient_list = [subscriber.email for subscriber in subscribers]
        subject = f'Special Treatment: {treatment.title}'
        from_email = settings.DEFAULT_FROM_EMAIL or 'noreply@thaisiam.com'
        
        for recipient in recipient_list:
            unsubscribe_url = f"{request.build_absolute_uri('/newsletter/unsubscribe/')}"
            book_now_url = f"{request.build_absolute_uri('/book-now/')}"
            
            context = {
                'treatment': treatment,
                'description': description,
                'unsubscribe_url': unsubscribe_url,
                'book_now_url': book_now_url,
            }
            html_content = render_to_string("newsletter/treatment_newsletter.html", context)
            
            email = EmailMultiAlternatives(subject, '', from_email, [recipient])
            email.attach_alternative(html_content, "text/html")
            try:
                email.send(fail_silently=False)
            except Exception as e:
                messages.error(request, f'Failed to send newsletter: {str(e)}')
                return redirect('dashboard:dashboard')
        
        messages.success(request, f'Newsletter sent to {len(recipient_list)} subscribers!')
        return redirect('dashboard:dashboard')
    
    return render(request, 'dashboard/send_newsletter.html', {'treatment': treatment})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    booking_datetime = datetime.combine(booking.date, booking.start_time)
    current_datetime = datetime.now()
    time_difference = booking_datetime - current_datetime
    
    if time_difference.total_seconds() < 24 * 3600: 
        messages.error(request, "You can only cancel bookings that are at least 24 hours away.")
        return redirect('dashboard:dashboard')
    
    if booking.status == 'cancelled':
        messages.warning(request, "This booking is already cancelled.")
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f"Your booking for {booking.treatment.title} on {booking.date} has been cancelled.")
        return redirect('dashboard:dashboard')
    
    return render(request, 'dashboard/cancel_booking.html', {'booking': booking})