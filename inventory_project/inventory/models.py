from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Currency(models.Model):
    code = models.CharField(max_length=3)  # e.g., 'NGN', 'USD'
    symbol = models.CharField(max_length=10)  # e.g., '₦', '$'

    def __str__(self):
        return self.code

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # New field for unit price
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Existing price field
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # New save method to calculate the total price
    def save(self, *args, **kwargs):
        self.price = self.quantity * self.unit_price  # Calculate total price
        super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return self.name


class Sale(models.Model):
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # New field for total price
    sale_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.item.unit_price  # Calculate total price for the sale
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale of {self.quantity} {self.item.name}(s)"
