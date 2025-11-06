from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, date
import uuid
from booking.models import Treatments, Booking
from booking.forms import BookingForm

def view_bag(request):
    return render(request, 'bag/bag.html')

def add_to_bag(request):
    if request.method == "POST":
            
        treatment_id = request.POST.get('treatment')
        date_str = request.POST.get('date')
        start_time = request.POST.get('start_time')
        duration = int(request.POST.get('duration'))
        
        booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if booking_date < date.today():
            messages.error(request, "You cannot book an appointment for a past date.")
            return redirect('book_now')
        
        treatment = Treatments.objects.get(id=treatment_id)
        if duration == 30:
            price = treatment.half_hour
        elif duration == 60:
            price = treatment.one_hour
        elif duration == 120:
            price = treatment.two_hour
        
        bag_item = {
            'id': str(uuid.uuid4()),
            'treatment_id': treatment.id,
            'treatment_title': treatment.title,
            'date': date_str,
            'start_time': start_time,
            'duration': duration,
            'price': float(price),
        }
        
        if 'bag' not in request.session:
            request.session['bag'] = []
        
        request.session['bag'].append(bag_item)
        request.session.modified = True
        
        return redirect('view_bag')
    return redirect('book_now')


@login_required
def view_bag(request):
    bag_items = request.session.get('bag', [])
    total_price = sum(item['price'] for item in bag_items)

    context = {
        'bag_items': bag_items,
        'total_price': total_price
    }

    return render(request, 'bag/bag.html', context)


def remove_from_bag(request, item_id):
    bag_items = request.session.get('bag', [])
    
    updated_bag_items = [
        item for item in bag_items if item.get('id') != item_id
    ]
    
    request.session['bag'] = updated_bag_items
    request.session.modified = True
    
    return redirect('view_bag')


@login_required
def edit_booking(request, item_id):
    item_id = str(item_id)
    bag_items = request.session.get('bag', [])
    item_to_edit = next((item for item in bag_items if str(item['id']) == item_id), None)

    if not item_to_edit:
        return redirect('view_bag')
    
    if request.method == 'POST':
        treatment_id = request.POST.get('treatment')
        date_str = request.POST.get('date')
        start_time = request.POST.get('start_time')
        duration = int(request.POST.get('duration'))

        booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if booking_date < date.today():
            messages.error(request, "You cannot book an appointment for a past date.")
            return redirect('view_bag')
        
        treatment = Treatments.objects.get(id=treatment_id)
        if duration == 30:
            price = treatment.half_hour
        elif duration == 60:
            price = treatment.one_hour
        elif duration == 120:
            price = treatment.two_hour

        for i, item in enumerate(bag_items):
            if str(item['id']) == item_id:
                bag_items[i].update({
                    'treatment_id': treatment.id,
                    'treatment_title': treatment.title,
                    'date': date_str,
                    'start_time': start_time,
                    'duration': duration,
                    'price': float(price),
                })
                break
        
        request.session['bag'] = bag_items
        request.session.modified = True
        return redirect('view_bag')
    else:

        form = BookingForm(initial={
            'treatment': item_to_edit['treatment_id'],
            'date': item_to_edit['date'],
            'start_time': item_to_edit['start_time'],
            'duration': item_to_edit['duration'],
        })

    treatments_list = Treatments.objects.all()
    context = {
        'form': form,
        'item_id': item_id,
        'item_to_edit': item_to_edit,
        'treatments': treatments_list
    }

    return render(request, 'bag/edit_booking.html', context)