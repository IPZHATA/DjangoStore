import pytest
from django.contrib.auth.models import User
from item.models import Item, Category
from order.models import Order, Address, OrderItem
from order.service import OrderService

@pytest.mark.django_db
class TestOrderService:
    def test_cancel_order(self):
        # Create a sample order
        user = User.objects.create_user(username='testuser')
        address = Address.objects.create(street='Test Street', city='Test City')
        order = Order.objects.create(user=user, address=address)

        # Cancel the order
        OrderService.cancel_order(order)

        # Check that the order is deleted
        assert not Order.objects.filter(pk=order.pk).exists()

    def test_create_order_from_items(self):
        user = User.objects.create_user(username='testuser')
        address = Address.objects.create(street='Test Street', city='Test City')

        category = Category.objects.create(name='Item 1')
        item1 = Item.objects.create(name='Item 1', category=category, created_by=user, price=10.0)
        item2 = Item.objects.create(name='Item 2', category=category, created_by=user, price=20.0)
        cart = [item1, item2]

        order = OrderService.create_order_from_items(user, address, cart)

        assert order.user == user
        assert order.address == address
        assert list(order.items.all()) == [
            OrderItem.create_order_item_from_item(order, item1),
            OrderItem.create_order_item_from_item(order, item2),
        ]

    def test_pay_for_order(self):
        # Create a sample order with items
        user = User.objects.create_user(username='testuser')
        address = Address.objects.create(street='Test Street', city='Test City')

        category = Category.objects.create(name='Item 1')
        item1 = Item.objects.create(name='Item 1', category=category, created_by=user, price=10.0)
        item2 = Item.objects.create(name='Item 2', category=category, created_by=user, price=20.0)
        order = Order.objects.create(user=user, address=address)
        OrderItem.create_order_item_from_item(order, item1).save()
        OrderItem.create_order_item_from_item(order, item2).save()

        # Pay for the order
        OrderService.pay_for_order(order)

        # Check that the order is paid and the total price is correct
        order.refresh_from_db()
        assert order.paid
        assert order.total_price == 30.0