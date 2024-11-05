from django.db import models
from .order import Order
from .barang import Barang

class Order(models.Model):
    # id = models.AutoField(unique=True, primary_key=True)
    id_order = models.ForeignKey(Order);
    nama_barang = models.ForeignKey(Barang);
    kuantitas = models.BigIntegerField();
    total_harga = models.BigIntegerField();

    def __str__(self):
        return self.id_user