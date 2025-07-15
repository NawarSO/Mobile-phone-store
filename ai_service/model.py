from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('CLIENT', 'Client'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CLIENT')
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class PhoneSpecs(models.Model):
    BRAND_CHOICES = [
        ('Samsung', 'Samsung'),
        ('Apple', 'Apple'),
        ('Xiaomi', 'Xiaomi'),
        ('Huawei', 'Huawei'),
        ('Oppo', 'Oppo'),
        ('Vivo', 'Vivo'),
        ('Other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES)
    model = models.CharField(max_length=100)
    ram = models.CharField(max_length=20)  
    storage = models.CharField(max_length=20)  
    screen_size = models.CharField(max_length=20) 
    condition = models.CharField(max_length=20, choices=[
        ('New', 'New'),
        ('Used', 'Used'),
        ('Refurbished', 'Refurbished')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    estimated_price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model}"



class Mobile(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cpu = models.CharField(max_length=100)
    ram = models.CharField(max_length=50)
    storage = models.CharField(max_length=50)
    screen_size = models.CharField(max_length=50)
    description = models.TextField()
    image_url = models.URLField()
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.brand} {self.model}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total(self):
        return sum(item.subtotal() for item in self.cartitem_set.all())

    def __str__(self):
        return f"Cart #{self.id} for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    mobile = models.ForeignKey(Mobile, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.mobile.price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.mobile.brand} {self.mobile.model}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_cancelled = models.BooleanField(default=False)

    def cancel_order(self):
        self.is_cancelled = True
        self.save()

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"