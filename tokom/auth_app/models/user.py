from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)  # This is already in AbstractUser

    def __str__(self):
        return self.username
