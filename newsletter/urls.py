from django.urls import path
from . import views


urlpatterns = [
    path('subscribe/', views.subscribe, name='subscribe'),
    path('unsubscribe/', views.unsubscribe_page, name='unsubscribe_page'),
    path('unsubscribe/confirm/', views.unsubscribe, name='unsubscribe'),
]
