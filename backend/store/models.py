from django.db import models
from decimal import *
from django.contrib.auth.models import User

class Book(models.Model):
    name: str = models.CharField(max_length=255)
    price: Decimal = models.DecimalField(max_digits=7, decimal_places=2)
    author: str = models.CharField(max_length=255)  
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f'Id {self.id}: {self.name}'