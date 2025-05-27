from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('treatments/', views.treatments, name='treatments'),
    path('book-now/', views.book_now, name='book_now'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('contact/', views.contact, name='contact'),
    path('terms-of-use/', views.coming_soon, name='terms_of_use'),
    path('privacy-policy', views.coming_soon, name='privacy_policy'),
]