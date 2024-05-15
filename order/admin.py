from django.contrib import admin
from .models import DeliveryProvider


@admin.register(DeliveryProvider)
class DeliveryOptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    list_editable = ['name', 'description']


# @admin.register(PaymentOption)
# class PaymentOptionAdmin(admin.ModelAdmin):
#     list_display = ['id', 'name', 'description']
#     list_editable = ['name', 'description']
