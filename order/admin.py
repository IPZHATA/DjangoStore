from django.contrib import admin
from .models import DeliveryOption, PaymentOption


@admin.register(DeliveryOption)
class DeliveryOptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    list_editable = ['name', 'description']


@admin.register(PaymentOption)
class PaymentOptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    list_editable = ['name', 'description']
