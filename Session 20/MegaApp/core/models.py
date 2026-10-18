from django.db import models
from django.utils import timezone
from datetime import timedelta
import random

# Custom User Model
class User(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    delivery_address = models.TextField(blank=True, default='')
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.name

# Task 1: Restaurant Model
class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    cuisine = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Task 2: Movie OTP Model (3-Min Expiry)
class MovieBookingOTP(models.Model):
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() <= self.created_at + timedelta(minutes=3)

    @classmethod
    def generate_otp(cls, email):
        code = str(random.randint(100000, 999999))
        return cls.objects.create(email=email, otp_code=code)

    def __str__(self):
        return f"{self.email} - {self.otp_code}"