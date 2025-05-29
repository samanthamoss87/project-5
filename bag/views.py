from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import uuid
from booking.models import Treatments

def view_bag(request):
    return render(request, 'bag/bag.html')

def add_to_bag(request):
    if request.method == "POST":
        treatment_id = request.POST.get('treatment')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        duration = int(request.POST.get('duration'))
        
        treatment = Treatments.objects.get(id=treatment_id)
        # Calculate price based on duration
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
            'date': date,
            'start_time': start_time,
            'duration': duration,
            'price': float(price),
        }
        
        # Initialize or update bag in session
        if 'bag' not in request.session:
            request.session['bag'] = []
        
        request.session['bag'].append(bag_item)
        request.session.modified = True
        
        return redirect('view_bag')
    return redirect('book_now')


@login_required
def view_bag(request):
    bag_items = request.session.get('bag', [])
    total = sum(item['price'] for item in bag_items)

    context = {
        'bag_items': bag_items,
        'total': total
    }

    return render(request, 'bag/bag.html', context)


def remove_from_bag(request, item_id):
    # Get the current items in the bag from the session
    bag_items = request.session.get('bag', [])
    
    # Check and remove the item with the matching item_id
    updated_bag_items = [
        item for item in bag_items if item.get('id') != item_id
    ]
    
    # Update the session with the new list
    request.session['bag'] = updated_bag_items
    request.session.modified = True
    
    return redirect('view_bag')