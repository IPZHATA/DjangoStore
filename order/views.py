from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from item.models import Item
from .models import Order, DeliveryProvider, OrderItem
from .forms import OrderForm, PaymentForm


def checkout(request):
    item = Item.objects.filter(is_sold=False)[0]
    items = [item, item, item]

    payment_form = PaymentForm()

    return render(request, "checkout.html",
                  {
                      "items": items,
                      "payment_form": payment_form
                  })
