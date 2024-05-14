from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from item.models import Item
from django.core.validators import MinValueValidator


class DeliveryOption(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural = "Delivery options"
        ordering = ["name"]

    def __str__(self):
        return self.name


class PaymentOption(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Payment options"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    delivery_option = models.ForeignKey(DeliveryOption, on_delete=models.PROTECT)
    payment_option = models.ForeignKey(PaymentOption, on_delete=models.PROTECT)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.user.name} - order id: {self.id}"

    @property
    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.SmallIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * Decimal(self.quantity)
