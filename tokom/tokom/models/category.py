from django.db import models

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name
