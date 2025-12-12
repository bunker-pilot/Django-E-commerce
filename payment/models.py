from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ShippingAddress(models.Model):
    full_name = models.CharField(max_length= 300)
    email = models.EmailField(max_length=255)
    address1 = models.CharField(max_length=300)
    address2 = models.CharField(max_length=300,blank=True , null=True)
    city = models.CharField(max_length=155)
    zip_code =models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name="shipping_address" , blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "Shipping Addresses"

    def __str__(self):
        return f"{self.full_name}-{self.city}"
    