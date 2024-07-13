from django.db import models
from .category import Category


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField(null=False)
    stock = models.IntegerField()
    description = models.TextField(max_length=500, blank=True, null=False)
    active = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, null=False, blank=False)