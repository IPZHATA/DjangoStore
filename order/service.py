from typing import List
from django.contrib.auth.models import User
from django.db import transaction
from item.models import Item
from order.models import Order, Address, OrderItem


class OrderService:

    @staticmethod
    def create_order_from_items(user: User, address: Address, cart: List[Item]) -> Order:
        """
        Starts transaction that creates order and
        order items in db, based on user, delivery address and
        list of items. Returns created order.
        """
        with transaction.atomic():
            address.save()
            order = Order.objects.create(user=user, address=address)
            for item in cart:
                order_item = OrderItem.create_order_item_from_item(order, item)
                order_item.save()
            order.save()
            return order

    @staticmethod
    def pay_for_order(order) -> None:
        """
        Starts transaction. Makes order paid status = True and saves
        total price on paying moment
        """
        with transaction.atomic():
            order.total_price = order.get_current_total_price()
            order.paid = True
            order.save()
