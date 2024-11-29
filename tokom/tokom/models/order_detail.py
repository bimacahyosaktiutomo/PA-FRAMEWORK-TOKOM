from django.db import models
from django.contrib.postgres.fields import ArrayField  # Optional, if you're using PostgreSQL
from .order import Order
from .item import Item

class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    
    # Store multiple items in a structured way as a JSONField
    items = models.JSONField()  # Stores a list of dictionaries with item details
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.order.id} - Items {len(self.items)}"
