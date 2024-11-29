from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Order(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('arrived', 'Arrived'),
    ]
    
    order_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    address = models.TextField(blank=True, null=True)
    total_price = models.BigIntegerField()  # This will store the total order price
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Ongoing')
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_created = models.DateTimeField(default=now, editable=False)  # Auto-set when the order is created
    date_arrived = models.DateField(blank=True, null=True)  # Set when the order is marked as "finished"

    def __str__(self):
        return f"Order {self.id} - User {self.user.username}"

    def update_total_price(self):
        # Calculate the total price of the order from the related OrderDetails
        total_price = sum(order_detail.total_price for order_detail in self.order_details.all())
        self.total_price = total_price
        self.save()
