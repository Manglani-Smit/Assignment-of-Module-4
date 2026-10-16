from django.db import models

# Custom User Model (Student Style)
class User(models.Model):
    USER_ROLES = (
        ('Buyer', 'Buyer'),
        ('Seller', 'Seller'),
    )
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    usertype = models.CharField(max_length=20, choices=USER_ROLES, default='Buyer')
    group_name = models.CharField(max_length=50, blank=True, null=True) # MovieCritic, MovieFan, Admin wagera ke liye

    def __str__(self):
        return f"{self.fname} {self.lname} ({self.email})"


# Q1: My Orders Model (Zomato Style)
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=100)
    items = models.TextField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.fname}"


# Q2: Product Model (Flipkart Style)
class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name


# Q3: Movie Review Model (BookMyShow Style)
class MovieReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=100)
    review_text = models.TextField()
    rating = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.movie_name} - {self.user.fname}"


# Q5: Playlist Model (Spotify Style)
class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=100)
    total_songs = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.playlist_name