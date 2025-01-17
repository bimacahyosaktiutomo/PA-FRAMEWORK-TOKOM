from django.db import models
from django.conf import settings
from .item import Item

class Review(models.Model):
    review_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.CharField(max_length=50)
    rating = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='reviews/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Review for {self.item.name} by {self.user.username}"
