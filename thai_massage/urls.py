from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from .views import custom_404

handler404 = 'thai_massage.views.custom_404'

urlpatterns = [
    path('', include('booking.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('bag/', include('bag.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('checkout/', include('checkout.urls')),
    path('newsletter/', include('newsletter.urls'))
]


