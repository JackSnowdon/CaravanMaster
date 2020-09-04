from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from accounts.models import Profile
from world.models import Location

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
    currently_at = models.ForeignKey(Location, related_name='games', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.owner.name}'s Caravan"


class MemberBase(models.Model):
    name = models.CharField(max_length=255)
    level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(50)], default=1)
    attack = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=0)
    defense = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=0)
    intel = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=0)
    cost = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=0)

    def __str__(self):
        return self.name


class CrewMember(models.Model):
    base = models.ForeignKey(MemberBase, related_name='members', on_delete=models.CASCADE)
    hired_by = models.ForeignKey(Avatar, related_name='crew', on_delete=models.CASCADE)
    max_hp = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=0)
    current_hp = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10000)], default=0)
    xp = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000000000)], default=0)
    assigned_to = models.ForeignKey(Caravan, related_name='guard', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.hired_by.name}'s {self.base.name}"

