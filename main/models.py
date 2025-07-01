from django.db import models
from django.contrib.auth.models import User

class Actor(models.Model):
    name=models.CharField(max_length=100)
    country=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    birthdate=models.DateField()

    def __str__(self):
        return self.name

class Movie(models.Model):
    name=models.CharField(max_length=100)
    genre=models.CharField(max_length=100)
    year=models.PositiveIntegerField()
    actors=models.ManyToManyField(Actor)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    name=models.CharField(max_length=100)
    price=models.FloatField()
    duration=models.DurationField()

    def __str__(self):
        return self.name

