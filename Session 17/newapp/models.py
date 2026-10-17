from django.db import models

class User(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.fname} {self.lname} ({self.email})"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.fname} - {self.product.name}"


class IPLTicketOrder(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.CharField(max_length=100, unique=True)
    gateway = models.CharField(max_length=20, default='Paytm') # Paytm ya PayPal
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_id} - {self.name} - {self.status}"