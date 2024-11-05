from django.db import models
from .kategori import Kategori

class Barang(models.Model):
    # id = models.AutoField(unique=True, primary_key=True)
    nama = models.CharField(max_length=13)
    deskripsi = models.CharField(max_length=255)
    kategori = models.ForeignKey(Kategori)
    rating = models.FloatField()
    stok = models.BigIntegerField()
    diskon = models.BigIntegerField()
    harga = models.BigIntegerField()
    image = models.ImageField(upload_to='Barang/')

    def __str__(self):
        return self.nama