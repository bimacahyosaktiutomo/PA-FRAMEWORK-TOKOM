from django.db import models
from .order import Order
from .item import Item

class OrderDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='order_details')
    quantity = models.BigIntegerField()
    total_price = models.BigIntegerField()

    def __str__(self):
        return f"OrderDetail {self.id} - Order {self.order.id}"
