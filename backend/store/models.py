from django.db import models
from decimal import *

class Book(models.Model):
    name: str = models.CharField(max_length=255)
    price: Decimal = models.DecimalField(max_digits=7, decimal_places=2)
    author: str = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'Id {self.id}: {self.name}'