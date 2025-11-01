from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Subscribe


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            subscriber, created = Subscribe.objects.get_or_create(email=email)
            if created:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': 'Successfully subscribed to our newsletter!'})
                messages.success(request, 'Successfully subscribed to our newsletter!')
            else:
                if subscriber.is_active:
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'message': 'You are already subscribed!'})
                    messages.info(request, 'You are already subscribed!')
                else:
                    subscriber.is_active = True
                    subscriber.save()
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({'success': True, 'message': 'Welcome back! You are now subscribed again.'})
                    messages.success(request, 'Welcome back! You are now subscribed again.')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Please enter a valid email address.'})
        return redirect('home')
    return redirect('home')


def unsubscribe_page(request):
    return render(request, 'newsletter/unsubscribe.html')


def unsubscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                subscriber = Subscribe.objects.get(email=email)
                subscriber.is_active = False
                subscriber.save()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': 'You have been unsubscribed successfully.'})
                messages.success(request, 'You have been unsubscribed successfully.')
            except Subscribe.DoesNotExist:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': 'Email not found in our subscription list.'})
                messages.error(request, 'Email not found in our subscription list.')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Please enter a valid email address.'})
        return redirect('unsubscribe_page')
    return redirect('unsubscribe_page')