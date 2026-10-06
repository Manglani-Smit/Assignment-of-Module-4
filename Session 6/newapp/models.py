from django.db import models

class User(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10)
    address = models.TextField(blank=True, null=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.fname


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    remarks = models.TextField()

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=150)
    cuisine = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.0)

    def __str__(self):
        return self.name