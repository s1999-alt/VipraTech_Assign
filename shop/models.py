from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
  name = models.CharField(max_length=100)
  price = models.DecimalField(max_digits=10, decimal_places=2)

  def __str__(self):
    return self.name
  

class Order(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField()
  total_amount = models.DecimalField(max_digits=10, decimal_places=2)
  payment_id = models.CharField(max_length=100, unique=True)
  paid = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.product.name} - {self.user.username if self.user else 'Guest'}"


