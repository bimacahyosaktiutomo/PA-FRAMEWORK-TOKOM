from django.db import models
from .category import Category

class Item(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=13)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    rating = models.FloatField(null=True, blank=True)
    stock = models.BigIntegerField(null=True, blank=True)
    discount = models.BigIntegerField(null=True, blank=True)
    price = models.BigIntegerField()
    image = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
