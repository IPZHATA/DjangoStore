from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from item.models import Item
from django.core.validators import MinValueValidator


class DeliveryProvider(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Delivery options"
        ordering = ["name"]

    def __str__(self):
        return self.name


# class PaymentOption(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         verbose_name_plural = "Payment options"
#         ordering = ["name"]
#
#     def __str__(self):
#         return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    delivery_option = models.ForeignKey(DeliveryProvider, on_delete=models.PROTECT)
    #payment_option = models.ForeignKey(PaymentOption, on_delete=models.PROTECT)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Order: {self.id} - By: {self.user.username} - Date: [{self.created_at}]"

    @property
    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.SmallIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"Order: {self.id} - By: {self.order.user.username}"

    def get_cost(self):
        return self.item.price * Decimal(self.quantity)

    def create_order_item_from_item(order, item):
        order_item = OrderItem.objects.create(
            order=order,
            item=item,
            quantity=1
        )
        return order_item
