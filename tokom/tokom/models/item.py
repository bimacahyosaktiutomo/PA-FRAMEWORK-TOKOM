from django.db import models
from .category import Category

class Item(models.Model):
    item_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=13)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    rating = models.FloatField(null=True, blank=True)
    # stock = models.ForeignKey('Stock', on_delete=models.CASCADE, null=True, blank=True, related_name='items')
    stock = models.BigIntegerField()
    discount = models.BigIntegerField(null=True, blank=True)
    price = models.BigIntegerField()
    image = models.ImageField(upload_to='items/')

    def __str__(self):
        return self.name


