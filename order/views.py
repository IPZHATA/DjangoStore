from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from item.models import Item
from .forms import AddressForm, PaymentForm
from .models import Order, OrderItem


@login_required()
def detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'detail.html', {'order': order})


@login_required()
def checkout(request):
    items = Item.objects.filter(is_sold=False)[0:2]
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            address = address_form.save()
            total_price = sum(item.price for item in items.all())
            order = Order.objects.create(user=request.user,
                                         address=address,
                                         total_price=total_price)
            for item in items:
                order_item = OrderItem.create_order_item_from_item(order, item)
                order_item.save()
            order.save()
            return redirect('order:payment', order.id)
    else:
        address_form = AddressForm()
    return render(request, "checkout.html", {"items": items, "address_form": address_form})


@login_required()
def payment(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if order.paid:
        return HttpResponse("You have already paid!")

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST, order=order)
        if payment_form.is_valid():
            order.paid = True
            order.save()
            return redirect('index')
    else:
        payment_form = PaymentForm(order=order)

    return render(request, 'payment.html', context={'form': payment_form})
