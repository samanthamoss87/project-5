from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('treatments/add/', views.add_treatment, name='treatment_add'),
    path('treatments/edit/<int:pk>/', views.edit_treatment, name='treatment_edit'),
    path('treatments/delete/<int:pk>/', views.delete_treatment, name='treatment_delete'),
]