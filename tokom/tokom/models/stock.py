from django.db import models
from .item import Item

class Stock(models.Model):
    id = models.BigAutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='stocks')  
    quantity = models.BigIntegerField()

    def __str__(self):
        return f"Stock for {self.item.name}"
