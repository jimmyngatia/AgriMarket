from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('Farmer', 'Farmer'),
        ('Buyer', 'Buyer'),
    ]
    
    full_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='Buyer'
    )
    
    def __str__(self):
        return f"{self.username} ({self.user_type})"
    
    def save(self, *args, **kwargs):
        # If full_name is provided, update first_name and last_name
        if self.full_name:
            name_parts = self.full_name.split(' ', 1)
            self.first_name = name_parts[0]
            if len(name_parts) > 1:
                self.last_name = name_parts[1]
        super().save(*args, **kwargs)


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Vegetables', 'Vegetables'),
        ('Fruits', 'Fruits'),
        ('Grains', 'Grains'),
        ('Dairy', 'Dairy'),
        ('Herbs', 'Herbs'),
        ('Other', 'Other'),
    ]
    
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} by {self.farmer.full_name or self.farmer.username}"
