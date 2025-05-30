from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout_view, name='checkout'),
    path('success/', views.payment_success, name='payment_success'),
    path('failed/', views.payment_failed, name='payment_failed'),
    
    # Webhooks
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
    
    # Testing
    path('test-stripe/', views.test_stripe_connection, name='test_stripe'),
    path('test-stripe/', views.test_stripe_connection, name='test_stripe'),
]