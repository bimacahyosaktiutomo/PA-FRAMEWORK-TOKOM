from django.db import models
from .barang import Barang 

class stok(models.Model):
    # id = models.AutoField(unique=True, primary_key=True)
    id_barang = models.ForeignKey(Barang, on_delete=models.CASCADE);
    jumlah = models.BigIntegerField();

    def __str__(self):
        return self.jumlah