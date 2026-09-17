from django.db import models

# Create your models here.

class Cuisine(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    rating = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.location} ({self.rating})"