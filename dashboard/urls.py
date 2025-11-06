from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('treatments/add/', views.add_treatment, name='treatment_add'),
    path('treatments/edit/<int:pk>/', views.edit_treatment, name='treatment_edit'),
    path('treatments/delete/<int:pk>/', views.delete_treatment, name='treatment_delete'),
    path('treatments/newsletter/<int:pk>/', views.send_newsletter, name='send_newsletter'),
    path('bookings/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]