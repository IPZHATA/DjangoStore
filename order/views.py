from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from item.models import Item
from .forms import AddressForm, PaymentForm


# def checkout(request):
#     item = Item.objects.filter(is_sold=False)[0]
#     items = [item, item, item]
#
#     payment_form = PaymentForm()
#     address_form = AddressForm()
#
#     return render(request, "checkout.html",
#                   {
#                       "items": items,
#                       "payment_form": payment_form,
#                       "address_form": address_form
#                   })

@login_required()
def checkout(request):

    item = Item.objects.filter(is_sold=False)[0]
    items = [item, item, item]

    if request.method == 'POST':
        address_form = AddressForm(request.POST, prefix='form_1')
        payment_form = PaymentForm(request.POST, prefix='form_2')
        if address_form.is_valid() and payment_form.is_valid():
            return redirect('item:index')
    else:
        address_form = AddressForm(prefix='form_1')
        payment_form = PaymentForm(prefix='form_2')

    return render(request, "checkout.html",
                  {
                      "items": items,
                      "payment_form": payment_form,
                      "address_form": address_form
                  })