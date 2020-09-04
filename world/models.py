from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=255)
    population = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000000)], default=1)
    prosperity = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    defense = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=0)

    def __str__(self):
        return self.name
