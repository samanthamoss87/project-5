from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from datetime import datetime
from .models import Order
from booking.models import Booking, Treatments

@receiver(post_save, sender=Order)
def send_order_confirmation_email(sender, instance, created, **kwargs):
    """Send confirmation email when order payment status changes to 'paid'"""
    if instance.payment_status == 'paid':
        try:
            create_bookings_from_order(instance)
            
            subject = f'Booking Confirmation - Thai Siam Massage #{instance.id}'
            from_email = settings.DEFAULT_FROM_EMAIL or 'noreply@thaisiam.com'
            to_email = [instance.email]
            
            user_bookings = Booking.objects.filter(user=instance.user, created_at__gte=instance.created_at)
            
            context = {
                'order': instance,
                'customer_name': instance.full_name,
                'order_total': instance.amount,
                'bookings': user_bookings,
            }
            
            html_content = render_to_string('checkout/order_confirmation_email.html', context)
            
            email = EmailMultiAlternatives(subject, '', from_email, to_email)
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=False)
            
        except Exception as e:
            print(f"Failed to send order confirmation email: {str(e)}")

def create_bookings_from_order(order):
    """Create actual booking records from order items"""
    try:
        for item in order.items.all():
            treatment = Treatments.objects.get(id=item.treatment_id)
            
            Booking.objects.create(
                user=order.user,
                treatment=treatment,
                date=datetime.strptime(item.date, '%Y-%m-%d').date() if isinstance(item.date, str) else item.date,
                start_time=datetime.strptime(item.start_time, '%H:%M').time() if isinstance(item.start_time, str) else item.start_time,
                duration=item.duration
            )
    except Exception as e:
        print(f"Failed to create bookings from order: {str(e)}")