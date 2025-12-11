from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ShippingAddressModel(models.Model):
    full_name = models.CharField(max_length= 300)
    email = models.EmailField(max_length=255)
    address1 = models.TextField()
    address2 = models.TextField()
    city = models.CharField(max_length=155)
    zip_code =models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return self.full_name
    