from django.db import models
from .barang import Barang

class Review(models.Model):
    # id = models.AutoField(unique=True, primary_key=True)
    barang_id = models.ForeignKey(Barang, on_delete=models.CASCADE)
    review = models.CharField(max_length=50)
    rating = models.FloatField()

    def __str__(self):
        return self.review