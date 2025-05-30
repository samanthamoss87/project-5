from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404


urlpatterns = [
    path('', include('booking.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('bag/', include('bag.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('checkout/', include('checkout.urls')),
]


handler404 = 'booking.views.custom_404'