from django.db import models
from django.conf import settings

class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    address = models.CharField(max_length=255, null=True)
    total_price = models.BigIntegerField()
    status = models.BooleanField()

    def __str__(self):
        return f"Order {self.id} - User {self.user.username}"
