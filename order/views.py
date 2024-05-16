from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from item.models import Item
from .forms import AddressForm, PaymentForm
from .models import Order, OrderItem
from .service import OrderService


@login_required()
def detail(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.user != order.user:
        return HttpResponseForbidden("You do not have permission to view this order.")

    return render(request, 'order/detail.html', {'order': order})


@login_required()
def checkout(request):
    items = Item.objects.filter(is_sold=False)[0:2]
    errors = []
    context = {'errors': errors, 'items': items}

    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            try:
                address = address_form.save(commit=False)
                order = OrderService.create_order_from_items(request.user, address, items)
                return redirect('order:payment', order.id)

            except Exception as e:
                errors.append('error occured when making transaction, try again later.')
    else:
        address_form = AddressForm()

    context['address_form'] = address_form
    return render(request, "order/checkout.html", context)


@login_required()
def payment(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.user != order.user:
        return HttpResponseForbidden("You do not have permission to view this order.")

    if order.paid:
        return HttpResponse("You have already paid!")

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST, order=order)
        if payment_form.is_valid():
            OrderService.pay_for_order(order)
            return redirect('index')
    else:
        payment_form = PaymentForm(order=order)

    return render(request, 'order/payment.html', context={'form': payment_form})
