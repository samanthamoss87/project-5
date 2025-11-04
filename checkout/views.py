from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

from .forms import CheckoutForm
from .models import Order, OrderItem


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

@login_required
def checkout_view(request):

    bag_items = request.session.get('bag', [])
    total_price = sum(float(item['price']) for item in bag_items)
    total_amount = int(total_price * 100)

    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)
        
        if form.is_valid():
            order = Order(
                user=request.user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                postal_code=form.cleaned_data['postal_code'],
                country=form.cleaned_data['country'],
                stripe_token=form.cleaned_data['stripe_token'],
                payment_status='pending',
                amount=total_price
            )
            order.save()

            for item in bag_items:
                OrderItem.objects.create(
                    order=order,
                    treatment_id=item['treatment_id'],
                    treatment_title=item['treatment_title'],
                    date=item['date'],
                    start_time=item['start_time'],
                    duration=item['duration'],
                    price=item['price']
                )

            try:
                payment_intent = stripe.PaymentIntent.create(
                    amount=total_amount,
                    currency='gbp',
                    description=f"Order #{order.id}",
                    payment_method=form.cleaned_data['stripe_token'],
                    confirm=True,
                    return_url=request.build_absolute_uri(f'/checkout/success/?order_id={order.id}')
                )
                
                order.payment_status = 'paid'
                order.stripe_payment_id = payment_intent.id
                order.save()

                if 'bag' in request.session:
                    del request.session['bag']
                    request.session.modified = True
                
                return redirect(f'/checkout/success/?order_id={order.id}')

            except stripe.error.CardError as e:
                messages.error(request, f"Payment failed: {e.error.message}")
                return redirect('checkout:checkout')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('checkout:checkout')
    else:
        form = CheckoutForm(user=request.user)

    context = {
        'form': form,
        'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY,
        'total_amount': total_amount,
        'total_price': total_price,
        'bag_items': bag_items,
    }
    
    return render(request, 'checkout/checkout.html', context)


@login_required
def payment_success(request):
    order_id = request.GET.get('order_id')
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        order = None

    return render(request, 'checkout/success.html', {'order': order})


def payment_failed(request):
    return render(request, 'checkout/failed.html')



def test_stripe_connection(request):
    stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
    try:
        account = stripe.Account.retrieve()
        return JsonResponse({'status': 'success', 'account': account})
    except stripe.error.StripeError as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        order = Order.objects.filter(stripe_payment_id=payment_intent['id']).first()
        if order:
            order.payment_status = 'paid'
            order.save()

    return HttpResponse(status=200)