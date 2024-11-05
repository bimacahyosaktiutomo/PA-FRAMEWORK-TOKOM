from django.db import models

class Kategori(models.Model):
    # id = models.AutoField(unique=True, primary_key=True)
    kategori = models.CharField(max_length=40)

    def __str__(self):
        return self.kategori