from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.fname} ({self.mobile})"

class PhoneOTP(models.Model):
    mobile = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_valid(self):
        # 5 minute ki validity aur unverified check
        expiry = self.created_at + timedelta(minutes=5)
        return timezone.now() <= expiry and not self.is_verified

    def __str__(self):
        return f"{self.mobile} - {self.otp}"