from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=500, blank=True, null=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
