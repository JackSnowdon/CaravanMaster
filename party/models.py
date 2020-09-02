from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from accounts.models import Profile

# Create your models here.

class Avatar(models.Model):
    name = models.CharField(max_length=255)
    level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)], default=1)
    attack = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=0)
    defense = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=0)
    intel = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=0)
    gold = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000000)], default=0)
    xp = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000000000)], default=0)
    created_by = models.ForeignKey(Profile, related_name='games', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Caravan(models.Model):
    owner = models.OneToOneField(Avatar, related_name='cav', on_delete=models.CASCADE)
    size = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=50)

    def __str__(self):
        return f"{self.owner.name}'s Caravan"


class Member(models.Model):
    name = models.CharField(max_length=255)
    level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)], default=1)
    attack = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=0)
    defense = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=0)
    intel = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=0)
    assigned_to = models.ForeignKey(Avatar, related_name='members', blank=True, null=True, on_delete=models.CASCADE)
    currently_in = models.ForeignKey(Caravan, related_name='crew', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
