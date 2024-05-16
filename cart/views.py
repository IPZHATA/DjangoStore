from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from order.models import Order, OrderItem
from item.models import Item


@login_required
def cart(request):
    current_user = request.user
    order = Order.objects.filter(user=current_user, paid=False).first()
    cart_items = order.items.all() if order else []
    total = sum(item.get_cost() for item in cart_items)

    return render(request, 'cart/cart.html', {
        "cart_empty": len(cart_items) == 0,
        "cart_items": cart_items,
        "total": total
    })


@login_required
def cart_add(request, product_id):
    current_user = request.user
    item = get_object_or_404(Item, id=product_id)

    order, created = Order.objects.get_or_create(user=current_user, paid=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, item=item)

    if not created:
        order_item.quantity += 1
        order_item.save()

    return redirect('cart:cart')


@login_required
def cart_remove(request, product_id):
    current_user = request.user
    order = Order.objects.filter(user=current_user, paid=False).first()
    if not order:
        return redirect('cart:cart')

    order_item = order.items.filter(item_id=product_id).first()
    if not order_item:
        return redirect('cart:cart')

    if order_item.quantity == 1:
        order_item.delete()
    else:
        order_item.quantity -= 1
        order_item.save()

    return redirect('cart:cart')


@login_required
def cart_remove_completely(request, product_id):
    current_user = request.user
    order = Order.objects.filter(user=current_user, paid=False).first()
    if not order:
        return redirect('cart:cart')

    order_item = order.items.filter(item_id=product_id).first()
    if order_item:
        order_item.delete()

    return redirect('cart:cart')
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import redirect, render
#
# from order.models import OrderItem
#
# @login_required
# def cart(request):
#     current_user_id = request.user.id
#     cart_items = CartItem.objects.filter(user_id=current_user_id)
#     total = sum(map(lambda cart_item: cart_item.get_total(), cart_items))
#     return render(request, 'cart/cart.html', {
#         "cart_empty": len(cart_items) == 0,
#         "cart_items": cart_items,
#         "total": total
#     })
#
#
# @login_required
# def cart_add(request, product_id):
#     current_user_id = request.user.id
#     cart_item = CartItem.objects.filter(user_id=current_user_id).filter(product_id=product_id).first()
#     if cart_item:
#         cart_item.quantity += 1
#         cart_item.save()
#     else:
#         CartItem.objects.create(user=request.user, product=product_id, quantity=1)
#
#     return redirect('cart:cart')
#
#
# @login_required
# def cart_remove(request, product_id):
#     current_user_id = request.user.id
#     cart_item = CartItem.objects.filter(user_id=current_user_id).filter(product_id=product_id).first()
#     if not cart_item:
#         return redirect('core:cart')
#
#     if cart_item.quantity == 1:
#         cart_item.delete()
#     else:
#         cart_item.quantity -= 1
#         cart_item.save()
#
#     return redirect('cart:cart')
#
#
# @login_required
# def cart_remove_completely(request, product_id):
#     current_user_id = request.user.id
#     cart_item = CartItem.objects.filter(user_id=current_user_id).filter(product_id=product_id).first()
#     if cart_item:
#         cart_item.delete()
#     return redirect('cart:cart')
