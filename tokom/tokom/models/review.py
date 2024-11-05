from django.db import models
from .item import Item

class Review(models.Model):
    id = models.BigAutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.CharField(max_length=50)
    rating = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Review for {self.item.name}"
