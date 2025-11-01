from django.contrib import admin
from .models import Subscribe

@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email',)