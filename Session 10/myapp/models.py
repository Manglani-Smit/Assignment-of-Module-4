from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    mobile = models.PositiveBigIntegerField()
    remarks = models.TextField()

    def __str__(self):
        return self.name

class User(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.PositiveBigIntegerField()
    address = models.TextField()
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.fname + " " + self.lname