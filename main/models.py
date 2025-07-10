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


class Review(models.Model):
    comment=models.TextField()
    rate=models.FloatField()
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name
