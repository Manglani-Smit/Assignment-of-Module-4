from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=150)
    cuisine = models.CharField(max_length=100)
    rating = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.cuisine} ({self.rating})"