from django.db import models

class Order(models.Model):
    # id = models.AutoField(unique=True, primary_key=True)
    id_user = models.ForeignKey();
    alamat = models.CharField(max_length=255);
    total_harga = models.BigIntegerField();
    status = models.BooleanField();

    def __str__(self):
        return self.id_user