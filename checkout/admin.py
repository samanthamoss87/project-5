from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'payment_status', 'created_at', 'updated_at')
    list_filter = ('payment_status', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'address')
